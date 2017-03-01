#!/bin/bash 

yesterday=`date -d '1 day ago' "+%Y%m%d"`
filename1="power_South_TpeMLXe8_${yesterday}.png"
filename2="power_South_ChiMLXe4_${yesterday}.png"
filename3="power_North_TpeMLXe8_${yesterday}.png"
filename4="power_North_ChiMLXe4_${yesterday}.png"

filename5="PowerDistribution_North_ChiMLXe4_${yesterday}.png"
filename6="PowerDistribution_North_TpeMLXe8_${yesterday}.png"
filename7="PowerDistribution_South_ChiMLXe4_${yesterday}.png"
filename8="PowerDistribution_South_TpeMLXe8_${yesterday}.png"

filename9="Flapping${yesterday}.png"
filename10="Flapping${yesterday}_duration_hist.png"
filename11="power_South_TpeMLXe8_${yesterday}_fullrange.png"
filename12="power_South_ChiMLXe4_${yesterday}_fullrange.png"
filename13="power_North_TpeMLXe8_${yesterday}_fullrange.png"
filename14="power_North_ChiMLXe4_${yesterday}_fullrange.png"
filename15="FlappingEventsTable_North_ChiMLXe4_${yesterday}.html"
filename16="FlappingEventsTable_North_TpeMLXe8_${yesterday}.html"
filename17="FlappingEventsTable_South_ChiMLXe4_${yesterday}.html"
filename18="FlappingEventsTable_South_TpeMLXe8_${yesterday}.html"

pass=`cat /nfs/home/zero/.ssh/passwd_ui02`
#convert $filename1 power_South_TpeMLXe8_*147*147*.png +append $filename1
#convert $filename2 power_South_ChiMLXe4_*147*147*.png +append $filename2
/usr/bin/expect exe2asgcui.exp $filename1 $filename2 $pass $yesterday
/usr/bin/expect exe2asgcui.exp $filename3 $filename4 $pass $yesterday
/usr/bin/expect exe2asgcui.exp $filename5 $filename6 $pass $yesterday
/usr/bin/expect exe2asgcui.exp $filename7 $filename8 $pass $yesterday
/usr/bin/expect exe2asgcui.exp $filename9 $filename10 $pass $yesterday
/usr/bin/expect exe2asgcui.exp $filename11 $filename12 $pass $yesterday
/usr/bin/expect exe2asgcui.exp $filename13 $filename14 $pass $yesterday
/usr/bin/expect exe2asgcui.exp $filename15 $filename16 $pass $yesterday
/usr/bin/expect  exe2asgcui.exp $filename17 $filename18 $pass $yesterday
