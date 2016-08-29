#!/bin/bash 

yday=`date -d '1 day ago' "+%Y%m%d"`
today=`date -d '' "+%Y%m%d"`
a=${yday:0:4}
b=${yday:4:2}
c=${yday:6:2}
filename1="south_route_TPEflapping_${yday}_log"
filename2="south_route_CHIflapping_${yday}_log"
tarfile="Flapping_figures_${yday}.tar.gz"
pass=`cat passwd`

/usr/bin/expect copyLogs.exp $a $b $c $pass

scp kschen@117.103.108.26:/root/Routers/Optical/TWBR2_Optical_$yday .
scp kschen@117.103.108.26:/root/Routers/Optical/CHIBR0_Optical_$yday .

cp CHIBR0_Optical_$yday CHIBR0_Optical_today
cp TWBR2_Optical_$yday TWBR2_Optical_today
