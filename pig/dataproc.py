#!/usr/bin/python
from org.apache.pig.scripting import *
import time
import sys
import os

INIT = Pig.compile("""
A = LOAD 'gs://page-rank-spark-bucket/small_page_links.nt' using PigStorage(' ') as (url:chararray, p:chararray, link:chararray);
B = GROUP A by url;                                                                                  
C = foreach B generate group as url, 1 as pagerank, A.link as links;                                 
STORE C into '$docs_in';
""")

UPDATE = Pig.compile("""
-- PR(A) = (1-d) + d (PR(T1)/C(T1) + ... + PR(Tn)/C(Tn))

previous_pagerank = 
    LOAD '$docs_in' 
    USING PigStorage('\t') 
    AS ( url: chararray, pagerank: float, links:{ link: ( url: chararray ) } );

outbound_pagerank =  
    FOREACH previous_pagerank 
    GENERATE 
        pagerank / COUNT ( links ) AS pagerank, 
        FLATTEN ( links ) AS to_url;

new_pagerank = 
    FOREACH 
        ( COGROUP outbound_pagerank BY to_url, previous_pagerank BY url INNER )
    GENERATE 
        group AS url, 
        ( 1 - $d ) + $d * SUM ( outbound_pagerank.pagerank ) AS pagerank, 
        FLATTEN ( previous_pagerank.links ) AS links;
        
STORE new_pagerank 
    INTO '$docs_out' 
    USING PigStorage('\t');
""")

params = { 'd': '0.85', 'docs_in': 'gs://page-rank-spark-bucket/out/pagerank_data_simple' }

start = time.time()

stats = INIT.bind(params).runSingle()
if not stats.isSuccessful():
      raise 'failed initialization'

nbIterations = 3
for i in range(nbIterations):
   out = "gs://page-rank-spark-bucket/out/pagerank_data_" + str(i + 1)
   params["docs_out"] = out
   Pig.fs("rmr " + out)
   stats = UPDATE.bind(params).runSingle()
   if not stats.isSuccessful():
      raise 'failed'
   params["docs_in"] = out

end = time.time()

SORT = Pig.compile("""
A = LOAD '$docs_in' 
    USING PigStorage('\t') 
    AS ( url: chararray, pagerank: float, links:{ link: ( url: chararray ) } );

sorted_pagerank = ORDER A BY pagerank DESC;

STORE sorted_pagerank 
    INTO '$docs_out' 
    USING PigStorage('\t');
""")

# We sort the last page rank in the bucket after the execution
out = "gs://page-rank-spark-bucket/out/pagerank_data_" + str(nbIterations) + "_sorted"
parameters = {'docs_in': params["docs_in"], 'docs_out' : out}
Pig.fs("rmr " + out)
stats = SORT.bind(parameters).runSingle()
if not stats.isSuccessful():
    raise 'failed sorted result'

# We delete the useless page rank file not sorted
Pig.fs("rmr " + params["docs_in"])

# We create a file in the bucket to store the execution time of the comput of the page rank
result = ("Execution time with pig was " + str(end - start) + " seconds.")
os.system("echo " + result)
name_file = "exec_time.txt"
with open(name_file, "a") as fichier:
    fichier.write(str(result))

call_with_args = "gsutil cp '%s' gs://page-rank-spark-bucket/" % (name_file)
os.system(call_with_args)