#!/bin/bash 

filenameBase=`date -d '1 day ago' "+%Y%m%d"`
filename1="south_route_TPEflapping_${filenameBase}_log"
filename2="south_route_CHIflapping_${filenameBase}_log"
tarfile="Flapping_figures_${filenameBase}.tar.gz"
pass=`cat passwd`
./copyRemote.exp $filename1 $filename2 $pass
