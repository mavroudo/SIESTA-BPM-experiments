#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 12 08:02:53 2024

@author: mavroudo
"""

import pandas as pd
import pm4py
import sys
import random

def append_df(original_df, appending_df, event_num):
    previous_ids = [i for i in original_df['case:concept:name']]
    # min_new_id = max(previous_ids) + 1
    x=random.sample("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",4)
    to_append_ids = appending_df['case:concept:name'].unique()
    map_ids = {tid: str(tid) + x for index, tid in enumerate(to_append_ids)}
    appending_df['case:concept:name'] = appending_df['case:concept:name'].map(map_ids)
    concated_df = pd.concat([original_df, appending_df], ignore_index=True)
    if concated_df.shape[0] > event_num:
        return concated_df.iloc[:event_num]
    return concated_df


if __name__ == "__main__":
    # filename = "data.xes"
    # event_num = 1000000
    filename = sys.argv[1]
    event_num = int(sys.argv[2])
    print("Loading dataset")
    log = pm4py.read_xes(filename)
    print("Converting to df")
    df = pm4py.convert.convert_to_dataframe(log)
    df = df[['case:concept:name', 'time:timestamp', 'concept:name']]
    events_in_log = df.shape[0]
    if event_num <= events_in_log:  # there are enough events
        df_new = df.iloc[:event_num]
    else:
        i = 0
        df_new = append_df(df, df.copy(deep=True), event_num)
        while df_new.shape[0] < event_num:
            print(f"Iteration {i} for appending new records. Size: {df_new.shape[0]}")
            df_new = append_df(df_new, df.copy(deep=True), event_num)
            i += 1
    print("Converting to log")
    log_final = pm4py.convert.convert_to_event_log(df_new)
    final_name = filename.split(".")[0] + f"_{str(event_num)}.xes"
    print("Writing log to file")
    pm4py.write.write_xes(log_final, final_name)
