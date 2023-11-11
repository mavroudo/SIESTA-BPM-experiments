import pandas as pd
from sqlalchemy import text

import declare_queries
import tqdm


def extract_precedence(engine, df: pd.DataFrame, support_threshold=0.9):
    activities = df["activity"].unique()
    pairs = [[i, j] for i in activities for j in activities]
    traces = len(df["case_id"].unique())
    results = []
    for pair in tqdm.tqdm(pairs, total=len(pairs), desc="Evaluating precedence rules"):
        connection = engine.connect()
        try:
            query = declare_queries.precedence(pair[0], pair[1], activities)
            rs = list(connection.execute(text(query)).all())
            x = pd.DataFrame(rs)
            containing_rule = 0 if len(x) == 0 else len(x["case_id"].unique())
            query2 = f"select case_id from events where activity = '{pair[0]}' group by case_id"
            did_not_activated = traces - len(list(connection.execute(text(query2)).all()))
            support = (containing_rule + did_not_activated) / traces
            if (support >= support_threshold):
                results.append(['precedence', pair[0], pair[1], support])
        finally:
            connection.close()
    return results
