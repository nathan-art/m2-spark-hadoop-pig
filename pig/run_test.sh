#!/bin/bash

## En local ->
## pig -x local -

## en dataproc...


## create the cluster
gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-central2 --zone europe-central2-c --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers 2 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project page-rank-spark

## copy data
gsutil cp small_page_links.nt gs://page-rank-spark-bucket/

## copy pig code
gsutil cp dataproc.py gs://page-rank-spark-bucket/

## Clean out directory
gsutil rm -rf gs://page-rank-spark-bucket/out


start=`date +%s`
## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pig --region europe-central2 --cluster cluster-a35a -f gs://page-rank-spark-bucket/dataproc.py

end=`date +%s`
echo Execution time was `expr $end - $start` seconds.

## access results
gsutil cat gs://page-rank-spark-bucket/out/pagerank_data_10/part-r-00000

## delete cluster...
gcloud dataproc clusters delete cluster-a35a --region europe-central2


exit `$end - $start`