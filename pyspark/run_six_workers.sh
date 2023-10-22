## Pour 6 workers

## copy data
gsutil cp small_page_links.nt gs://large_scale_data/

## copy pig code
gsutil cp pagerank-notype.py gs://large_scale_data/

## Clean out directory
gsutil rm -rf gs://large_scale_data/pyspark_result_


## create the cluster
gcloud dataproc clusters create cluster-a35a --enable-component-gateway --region europe-central2 --zone europe-central2-c --master-machine-type n1-standard-4 --master-boot-disk-size 500 --num-workers 6 --worker-machine-type n1-standard-4 --worker-boot-disk-size 500 --image-version 2.0-debian10 --project large-scale-data-401112


## run
## (suppose that out directory is empty !!)
gcloud dataproc jobs submit pyspark --region europe-central2 --cluster cluster-a35a gs://large_scale_data/pagerank-notype.py  -- gs://large_scale_data/small_page_links.nt 3 6

## access results
# gsutil cat gs://large_scale_data/out/pagerank_data_10/part-r-00000

## delete cluster...
gcloud dataproc clusters delete cluster-a35a --region europe-central2