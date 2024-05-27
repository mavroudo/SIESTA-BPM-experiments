# SIESTA-BPM-experiments
This repository contains the code for solutions that extract Declare patterns from event logs. The 5 different systems are:
* Declare4py: a python library. The script for evaluating this system is located in `declare4py/evaluation/evaluate.py`.
* Neo4j: a graph-based approach. The script for evaluating this system is located in `neo4j-bpm-declare/graph-encoded.py`
* Match_Recognize: an sql operator implemented on Trino (using a postgres db). The script for evaluating this system is located in `match-recognize/trino_implementation.py`
* RuM: a desktop application. We utilize the jar (version 0.7.2) from `https://rulemining.org/`
* SIESTA-bpm: our approach, which is an implementation of business process mining on top of a scalable system named SIESTA.
The code of the preprocessing component is the same that the authors of SIESTA used and can be found in ```https://github.com/mavroudo/SequenceDetectionPreprocess/tree/2.2.0```. Our new version of the query processor is available at ```https://anonymous.4open.science/r/SequenceDetectionQueryExecutor-046B```.

A step-by-step guide on how to execute our method, can be found inside the `siesta-bpm-experiments/`.

For the Neo4j and Match_Recognize we also provide the docker compose which is responsible to
deploy the required services.
