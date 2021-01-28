#!/bin/bash

if [[ $# -ne 1 ]]; then
    echo "Illegal number of parameters. Scicat token expected as first argument."
    exit 2
fi

SIMULATION=""
NUMBEROFTHUMBNAILS="4"
VERBOSELEVEL="0"  # 0,1,2
ACCESSGROUPS="public it wb hasylab external"

cmd="/home/lucaschr/.conda/envs/py35/bin/python"

# Delete all existing data

script="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/_delete_all_models.py"

args="samples sampleId"
$cmd $script $1 $args $SIMULATION

args="proposals proposalId"
$cmd $script $1 $args $SIMULATION

args="datasets pid"
$cmd $script $1 $args $SIMULATION

args="origdatablocks id"
$cmd $script $1 $args $SIMULATION

args="attachments id"
$cmd $script $1 $args $SIMULATION

# Add samples

script="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/_add_samples.py"

$cmd $script $1 _samples_synchroload.csv 0 7 6 $SIMULATION
$cmd $script $1 _samples_mgbone.csv 0 4 9 $SIMULATION
$cmd $script $1 _samples_ztl.csv 0 $SIMULATION

# Ingestion

argsp="hasylab julian.moosmann@desy.de"
argso="-n ${NUMBEROFTHUMBNAILS} -b -v ${VERBOSELEVEL} -a ${ACCESSGROUPS}"

p05="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestP05.py"
p07="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestP07.py"
pvj="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestResampled.py"
pvb="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestRegistered.py"
pvs="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestSegmented.py"
pvz="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestZTL.py"

$cmd $p05 $1 $argsp 11001978 2016 $argso $SIMULATION 
$cmd $p05 $1 $argsp 11003288 2017 $argso $SIMULATION
$cmd $p05 $1 $argsp 11003440 2017 $argso $SIMULATION
$cmd $p05 $1 $argsp 11003773 2017 $argso $SIMULATION
$cmd $p05 $1 $argsp 11003950 2017 $argso $SIMULATION
$cmd $p05 $1 $argsp 11004016 2017 $argso $SIMULATION
$cmd $p05 $1 $argsp 11004263 2018 $argso $SIMULATION
$cmd $p05 $1 $argsp 11004936 2018 $argso $SIMULATION
$cmd $p05 $1 $argsp 11005553 2018 $argso $SIMULATION
$cmd $p05 $1 $argsp 11005842 2019 $argso $SIMULATION
$cmd $p07 $1 $argsp 11006991 2019 $argso $SIMULATION -k tomography

$cmd $pvj $1 $argsp 11001978 2016 p05 $argso $SIMULATION -m -k resampled

$cmd $pvs $1 $argsp _segmented_list.csv $argso $SIMULATION

argsp="hasylab berit.zeller-plumhoff@hzg.de"
$cmd $pvb $1 $argsp 11005218 2018 p03 _histo_srct_registered.csv $argso $SIMULATION -m -e .tif .tiff .img .ndpi .vgl .svg .png -u Inkscape VGStudio

argsp="hasylab christian.lucas@desy.de"
$cmd $pvz $1 $argsp $argso $SIMULATION -k labMR MRI