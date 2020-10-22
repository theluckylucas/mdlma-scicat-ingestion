#!/bin/bash

cmd="/home/lucaschr/.conda/envs/py35/bin/python"
p05="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestP05.py"
p07="/home/lucaschr/TemporalStorage/mdlma-scicat-ingestion/IngestP07.py"
token="cTWpGkDDpalPke7TkdGmQlKa4GYFAwNtf5RhRE7QUVgTwXH01S3tDrqnkSIYKPqW"
argsp="hasylab julian.moosmann@desy.de"
argso="-n 4 -b -v 0"

$cmd $p05 $argsp 11004936 2018 $argso 
$cmd $p05 $argsp 11004263 2018 $argso 
$cmd $p05 $argsp 11004016 2017 $argso 
$cmd $p05 $argsp 11003288 2017 $argso 
$cmd $p05 $argsp 11003440 2017 $argso 
$cmd $p05 $argsp 11005553 2018 $argso 
$cmd $p05 $argsp 11003950 2017 $argso 
$cmd $p05 $argsp 11003773 2017 $argso 
$cmd $p05 $argsp 11001978 2016 $argso 
$cmd $p05 $argsp 11006991 2019 $argso 
$cmd $p05 $argsp 11005842 2019 $argso 
$cmd $p07 $argsp 11006991 2019 $argso -k tomography