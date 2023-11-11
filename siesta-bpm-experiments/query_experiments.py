#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  3 09:42:21 2023

@author: mavroudo
"""
import requests
datasets = ["bpi_2017","bpi_2018","bpi_2019"]
#datasets = ["test"]
#url = "http://anaconda.csd.auth.gr:8080/declare"
url = "http://localhost:8090/declare"
endpoints= ["/positions","/existences","/ordered-relations","/"]

constraints={0:["first","last","both"],1:["existence","absence","exactly","co-existence",
             "choice","exclusive-choice","responded-existence"], 2:["simple-response",
                                                              "simple-precedence", "simple-succession","alternate-response",
                                                              "alternate-precedence", "alternate-succession","chain-response",
                                                              "chain-precedence", "chain-succession"]}
support=0.9
exported_file="results_from_home.txt"

def create_params(dataset, support,  index, option:str):
    params = {"support":support, "log_database": dataset}
    if index==0:
        params["position"]=option
    elif index==1:
        params["modes"]=option
    elif index==2:
        o=option.split("-")
        params["mode"]=o[0]
        params["constraint"]=o[1]
    return params
    
with open(exported_file,"a+") as f:
    f.write("{},{},{},{},{}\n".format("Dataset","Endpoint","Support","Option","Time"))

for d in datasets:
    for  i in range(len(endpoints)):
        u = url+endpoints[i]
        print(u)
        if i!=3: #except for the all together query
            options = constraints[i]
            for o in options:
                params=create_params(d,support,i,o)
                resp = requests.get(u, params=params)
                print(resp.content)
                secs = resp.elapsed.total_seconds()
                with open(exported_file,"a+") as f:
                    f.write("{},{},{},{},{}\n".format(d,endpoints[i][1:],support,o,secs))
        else:
            params=create_params(d,support,i,"")
            resp = requests.get(u, params=params)
            secs = resp.elapsed.total_seconds()
            with open(exported_file,"a+") as f:
                f.write("{},{},{},{},{}\n".format(d,"all",support,"all",secs))
