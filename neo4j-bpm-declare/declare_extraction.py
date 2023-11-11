from tqdm import tqdm


def precedence(driver, unique_activities, total_traces, support=0.9):
    # create all pairs
    pairs = [[a, b] for a in unique_activities for b in unique_activities]  # n^2 test all possible things
    query = """
        Match (c:Case) where (c)<-[:EVENT_TO_CASE]-(:Event{activity: $activity_b }) 
        and not exists ((c)<-[:EVENT_TO_CASE]-(:Event{activity: $activity_a }))
        return distinct c.case_id as case_id
        union all
        Match (a:Event{activity:$activity_a })-[:EVENT_TO_CASE]->(c), (c)<-[:EVENT_TO_CASE]-(b:Event{activity:$activity_b})
        where a.position > b.position 
        return distinct c.case_id as case_id
    """
    result_set = []
    for pair in tqdm(pairs, total=len(pairs), desc="Extracting Precedence rules"):
        records, summary, k = driver.execute_query(query, activity_a=pair[0], activity_b=pair[1])
        if len(records) / total_traces >= support:
            result_set.append(pair)
    return result_set
