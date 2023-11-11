#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 09:11:05 2023

@author: mavroudo
"""
import  numpy as np
import requests
datasets = ["bpi_2017","bpi_2018","bpi_2019"]
#datasets = ["test"]
#url = "http://anaconda.csd.auth.gr:8080/declare"
url = "http://localhost:8090/declare/"


def create_params(dataset, support):
    params = {"support":support, "log_database": dataset}
    return params
    

with open("results_multiple_supports.txt","a+") as f:
    for dataset in datasets:
        for support in np.arange(0.8,0.9,0.01):
            params=create_params(dataset,support)
            resp = requests.get(url, params=params)
            secs = resp.elapsed.total_seconds()
            f.write("siesta,{},{},{:.2f}\n".format(dataset.split("_")[1],support,secs))
