from src.declare4py.declare4py import Declare4Py
import time
import sys

s_start = time.time()
start = time.time()
d4py = Declare4Py()
d4py.parse_xes_log(sys.argv[1])
print(len(d4py.log))
print(time.time() - start)

# basic statistics
# Return the number of cases in the log
print(f"Number of cases: {d4py.get_log_length()}")
print("--------------------------------------")

# Return the names of the activities in the log
print(f"Activity alphabet:\n{d4py.get_log_alphabet_activities()}")
print("--------------------------------------")

# Frequent Itemsets -> are they concecutive?
start = time.time()
d4py.compute_frequent_itemsets(min_support=0.5, len_itemset=2)
print(f"Frequent itemsets found: {len(d4py.frequent_item_sets)}")
print(time.time() - start)

# discover declare
start = time.time()
discovery_results = d4py.discovery(consider_vacuity=False, max_declare_cardinality=2)
print(d4py.filter_discovery(min_support=0.9))
print(time.time() - start)

print(f"Total time: {time.time() - s_start} seconds")