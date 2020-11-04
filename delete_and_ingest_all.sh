#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Illegal number of parameters. Scicat token expected as first argument."
    exit 2
fi

NUMBEROFTHUMBNAILS="4"
VERBOSELEVEL="0"  # 0,1,2

echo "Scicat token expected as first argument"

cmd="/home/lucaschr/.conda/envs/py35/bin/python"

# Delete all existing data

script="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/_delete_all_models.py"

$cmd $script $1 "samples sampleId"
$cmd $script $1 "proposals proposalId"
$cmd $script $1 "datasets pid"
$cmd $script $1 "origdatablocks id"
$cmd $script $1 "attachment id"

# Add samples

script="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/_add_samples.py"

$cmd $script $1 _samples_synchroload.csv 0 7 6
$cmd $script $1 _samples_mgbone.csv 0 7 6

# Ingestion

p05="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestP05.py"
p07="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestP07.py"
argsp="hasylab julian.moosmann@desy.de"
argso="-n ${NUMBEROFTHUMBNAILS} -b -v ${VERBOSELEVEL}"

$cmd $p05 $1 $argsp 11004936 2018 $argso 
$cmd $p05 $1 $argsp 11004263 2018 $argso 
$cmd $p05 $1 $argsp 11004016 2017 $argso 
$cmd $p05 $1 $argsp 11003288 2017 $argso 
$cmd $p05 $1 $argsp 11003440 2017 $argso 
$cmd $p05 $1 $argsp 11005553 2018 $argso 
$cmd $p05 $1 $argsp 11003950 2017 $argso 
$cmd $p05 $1 $argsp 11003773 2017 $argso 
$cmd $p05 $1 $argsp 11001978 2016 $argso 
$cmd $p05 $1 $argsp 11006991 2019 $argso 
$cmd $p05 $1 $argsp 11005842 2019 $argso 
$cmd $p07 $1 $argsp 11006991 2019 $argso -k tomography

pvj="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestResampled.py "

$cmd $pvj $1 $argsp 11001978 2016 p05 $argso -m -k resampled
