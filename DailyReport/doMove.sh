#!/bin/bash 

filenameBase=`date -d '1 day ago' "+%Y%m%d"`
filename1="south_route_TPEflapping_${filenameBase}_log"
filename2="south_route_CHIflapping_${filenameBase}_log"
tarname="Flapping_figures_${filenameBase}.tar.gz"

mv $filename1 logbackup
mv $filename2 logbackup
tar czf $tarname Flapping*png 
