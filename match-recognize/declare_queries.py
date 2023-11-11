def precedence(activity_a: str, activity_b: str, activity_all: list):
    x = ",".join([f"'{a}'" for a in activity_all])
    return f"""select * from events
        Match_recognize(
            partition by case_id
            Measures 
                A.case_id as trace,
                A.timestamp as starting,
                B.timestamp as ending
            one row per match
            after match skip past last row
            Pattern (A We*? B)
            Define 
                A as activity = '{activity_a}',
                B as activity = '{activity_b}',
                We as activity in ({x})
        )
    """
