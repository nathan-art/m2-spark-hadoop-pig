#!/bin/bash

## create the cluster
gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-central2 --zone europe-central2-b --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers $1 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project page-rank-spark

# Normally, the bucket used has already this 2 files.
## copy data
#gsutil cp small_page_links.nt gs://page-rank-spark-bucket/
## copy pig code
#gsutil cp dataproc.py gs://page-rank-spark-bucket/

## Clean out directory
gsutil rm -rf gs://page-rank-spark-bucket/out


start=`date +%s`
## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pig --region europe-central2 --cluster cluster-a35a -f gs://page-rank-spark-bucket/dataproc.py

end=`date +%s`
echo Execution time with pig and $1 workers was `expr $end - $start` seconds. >> results.txt

## access results
gsutil cat gs://page-rank-spark-bucket/out/pagerank_data_simple/part-r-00000 >> pig_small_page_rank.txt

## delete cluster...
gcloud dataproc clusters delete cluster-a35a --region europe-central2
