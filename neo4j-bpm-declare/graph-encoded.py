import pm4py
import pandas as pd
from neo4j import GraphDatabase
from time import time
import sys
import declare_extraction


def create_csv_file(filename):
    log = pm4py.read_xes(filename)
    d = []
    global_id = 1
    for t in log:
        for index, event in enumerate(t):
            event["position"] = index + 1
            event["id"] = global_id
            global_id += 1
            event["case:concept:name"] = t.attributes["concept:name"]
            d.append(event)
    df: pd.DataFrame = pd.DataFrame(d)
    df = df[["id", "concept:name", "time:timestamp", "case:concept:name", "position"]]
    df.columns = ["id", "activity", "timestamp", "case", " position"]
    df.to_csv("import/" + filename.split(".")[0] + ".csv")


# load data
def import_cases(session, filename: str):
    session.run("""
        LOAD CSV WITH HEADERS
        FROM $filename as line
        CALL{
            WITH line
            MERGE (c:Case {case_id:line.case})
        } IN TRANSACTIONS OF 500 ROWS     
    """, filename=f"file:///{filename}")


def import_events(tx, filename: str):
    file = "file:///" + filename
    tx.run("""
        LOAD CSV WITH HEADERS
        FROM $file as line
        CALL{
            WITH line
            MATCH(c: Case{case_id: line.case})
            CREATE (e:Event {event_id:toInteger(line.id), activity:line.activity, timestamp:line.timestamp,
            position:toInteger(line.position)})
            CREATE(e) - [: EVENT_TO_CASE]->(c)
        } IN TRANSACTIONS OF 1000 ROWS
        """, file=file)


def clean_database(session):
    session.run("MATCH (a)-[r]->() DELETE a,r")
    session.run("MATCH (n) DELETE n")
    try:
        session.run("DROP CONSTRAINT unique_events IF EXISTS")
        session.run("DROP CONSTRAINT unique_cases IF EXISTS")
        pass
    except:
        pass


filename = sys.argv[1]

csv_file = filename.split(".")[0] + ".csv"
uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "testneo4j"), max_connection_lifetime=200)
driver.verify_connectivity()
with driver.session() as session:
    start = time()
    create_csv_file(filename)
    print("Cleaning database...")
    clean_database(session)
    driver.execute_query("""CREATE CONSTRAINT unique_events FOR (e:Event) REQUIRE e.event_id IS UNIQUE""")
    driver.execute_query("""CREATE CONSTRAINT unique_cases FOR (c:Case) REQUIRE c.case_id IS UNIQUE""")
    print("Importing cases...")
    import_cases(session, csv_file)
    print("Importing events...")
    import_events(session, csv_file)
    print(f"Loading time: {time() - start} seconds")
    pass

df = pd.read_csv("import/" + csv_file)
unique_activities = list(df["activity"].unique())
total_traces = len(df["case"].unique())
declare_extraction.precedence(driver, unique_activities, total_traces)
