#!/bin/bash

## create the cluster
gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-central2 --zone europe-central2-b --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers $1 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project page-rank-spark

# Normally, the bucket used has already this 3 files.
## copy small data
#gsutil cp small_page_links.nt gs://page-rank-spark-bucket/
## copy big data
#gsutil cp gs://public_lddm_data/page_links_en.nt.bz2 gs://page-rank-spark-bucket/
## copy pig code
#gsutil cp dataproc.py gs://page-rank-spark-bucket/

## Clean out directory
gsutil rm -rf gs://page-rank-spark-bucket/out


## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pig --region europe-central2 --cluster cluster-a35a -f gs://page-rank-spark-bucket/dataproc.py

# access time execution result and add the number of workers for this execution
gsutil cat gs://page-rank-spark-bucket/exec_time.txt >> time_results.txt

# Use sed to add the text at the end of the last line of the file
sed -i "\$s/$/ (with $1 workers)/" time_results.txt
echo "" >> time_results.txt

## Save top page rank
gsutil cat gs://page-rank-spark-bucket/top_5_page_rank/part-r-00000 >> pig_top_page_rank.txt

## delete cluster...
gcloud dataproc clusters delete cluster-a35a --region europe-central2
