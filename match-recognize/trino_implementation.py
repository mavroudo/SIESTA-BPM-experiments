from sqlalchemy import create_engine, Table, Column, Integer, String, text
from sqlalchemy.orm import declarative_base
from sqlalchemy import MetaData, insert
from sqlalchemy.orm import sessionmaker
import pm4py
import time
import extract_rules
from Event import Event
from Event import Base
import sys
import trino

file = sys.argv[1]
# engine = create_engine('trino://trino@localhost:8080/mysql/tiny', echo=True)
engine = create_engine('postgresql+psycopg2://admin:admin@localhost:5432/postgres')
connection = engine.connect()
table_name = file.split('.')[0]


def clean_database(engine):
    metadata = MetaData()
    base = declarative_base()
    metadata.reflect(bind=engine)
    table = metadata.tables.get("events")
    if table is not None:
        base.metadata.drop_all(engine, [table], checkfirst=True)


clean_database(engine)
Base.metadata.create_all(bind=engine)
start = time.time()
log = pm4py.read_xes(file)
df = pm4py.convert_to_dataframe(log)
ids = [i for i in range(1, int(df.shape[0]) + 1)]
df["id"] = ids
df = df[["id", "concept:name", "time:timestamp", "case:concept:name"]]
df.columns = ["id", "activity", "timestamp", "case_id"]

x = df.to_dict('records')
Session = sessionmaker(engine)
with Session() as session:
    session.execute(insert(Event), x)
    session.commit()
print(f"Loading log: {time.time() - start} seconds")

activities = df["activity"].unique()
engine2 = create_engine('trino://trino@localhost:8080/postgres/public')
precedence = extract_rules.extract_precedence(engine2, df, 0.9)
#print(precedence)
