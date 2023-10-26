#
# Licensed to the Apache Software Foundation (ASF) under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

"""
This is an example implementation of PageRank. For more conventional use,
Please refer to PageRank implementation provided by graphx

Example Usage:
bin/spark-submit examples/src/main/python/pagerank.py data/mllib/pagerank_data.txt 10
"""
import re
import sys
from operator import add
from typing import Iterable, Tuple

import time
import json
from subprocess import call

from pyspark.resultiterable import ResultIterable
from pyspark.sql import SparkSession


# removed typing for compatibility with Spark 3.1.3
# typing ok with spark 3.3.0

def computeContribs(urls, rank):
    """Calculates URL contributions to the rank of other URLs."""
    num_urls = len(urls)
    for url in urls:
        yield (url, rank / num_urls)


def parseNeighbors(urls):
    """Parses a urls pair string into urls pair."""
    parts = re.split(r'\s+', urls)
    return parts[0], parts[2]


if __name__ == "__main__":

    # this file takes 3 parameters, the file where the pagerank will be executed, the number of pagerank iterations and the number of workers in the cluster used for the execution of this python file
    if len(sys.argv) != 4:
        print("Usage: pagerank <file> <iterations> <num_workers>", file=sys.stderr)
        sys.exit(-1)

    print("WARN: This is a naive implementation of PageRank and is given as an example!\n" +
          "Please refer to PageRank implementation provided by graphx",
          file=sys.stderr)

    statistics_time = {}
    bucket = "gs://large_scale_data"

    # Initialize the spark context.
    spark = SparkSession \
        .builder \
        .appName("PythonPageRank") \
        .getOrCreate()

    # This is where the timestamp of the pagerank execution begins
    start_program_timestamp = time.time()

    # Loads in input file. It should be in format of:
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     URL         neighbor URL
    #     ...
    lines = spark.read.text(sys.argv[1]).rdd.map(lambda r: r[0])

    # Loads all URLs from input file and initialize their neighbors.
    links = lines.map(lambda urls: parseNeighbors(urls)).distinct().groupByKey().cache()

    # Loads all URLs with other URL(s) link to from input file and initialize ranks of them to one.
    ranks = links.map(lambda url_neighbors: (url_neighbors[0], 1.0))

    # Partitioning of links
    links = links.partitionBy(numPartitions=None)

    # Calculates and updates URL ranks continuously using PageRank algorithm.
    for iteration in range(int(sys.argv[2])):
        # Partitioning of ranks
        ranks = ranks.partitionBy(numPartitions=None)

        # Calculates URL contributions to the rank of other URLs.
        contribs = links.join(ranks).flatMap(lambda url_urls_rank: computeContribs(
            url_urls_rank[1][0], url_urls_rank[1][1]  # type: ignore[arg-type]
        ))

        # Re-calculates URL ranks based on neighbor contributions.
        ranks = contribs.reduceByKey(add).mapValues(lambda rank: rank * 0.85 + 0.15)

    # Write and save pyspark results in a bucket
    ranks.coalesce(1).saveAsTextFile(bucket + "/pyspark_result_")

    print("Résultats pyspark écrits")

    spark.stop()

    # This is where the timestamp of the pagerank execution ends
    finish_program_timestamp = time.time()

    total_time_elapsed = finish_program_timestamp - start_program_timestamp


    statistics_time['start_program_timestamp'] = start_program_timestamp
    statistics_time['finish_program_timestamp'] = finish_program_timestamp
    statistics_time['total_time_elapsed'] = finish_program_timestamp - start_program_timestamp

    # the begin, end and total duration of the pagerank execution is stored in a json file, because it is simpler to collect to make the comparison graph of duration
    statistics_filename = 'pyspark_statistics_num_workers_' + sys.argv[3] + '.json'

    with open(statistics_filename, 'w+') as outfile:
        outfile.write(json.dumps(statistics_time))

    # copy the json file in the bucket
    call(["gsutil", "cp", statistics_filename, bucket])
