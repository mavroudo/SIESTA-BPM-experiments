#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 09:11:05 2023

@author: mavroudo
"""
import  numpy as np
import requests
#datasets = ["bpi_2017","bpi_2018","bpi_2019"]
#datasets = ["test"]
#url = "http://anaconda.csd.auth.gr:8080/declare"
url = "http://localhost:8090/declare/"


def create_params(dataset, support):
    params = {"support":support, "log_database": dataset}
    return params
    

#with open("results_multiple_supports.txt","a+") as f:
#    for dataset in datasets:
#        for support in np.arange(0.8,0.9,0.01):
#            params=create_params(dataset,support)
#            resp = requests.get(url, params=params)
#            secs = resp.elapsed.total_seconds()
#            f.write("siesta,{},{},{:.2f}\n".format(dataset.split("_")[1],support,secs))
support=0.9
datasets = ["bpi_1000","bpi_10000","bpi_100000","bpi_1000000"]
with open("scalability.txt","a+") as f:
    for dataset in datasets:
        print(dataset)
        params=create_params(dataset,support)
        resp = requests.get(url, params=params)
        secs = resp.elapsed.total_seconds()
        print(secs)
        f.write("siesta,{},{},{:.2f}\n".format(dataset.split("_")[1],support,secs))


params=create_params("bpi_1000",0.9)
resp = requests.get(url, params=params)