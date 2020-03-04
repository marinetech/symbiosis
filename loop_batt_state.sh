#!/bin/bash

LOG_FILE="out.csv"

echo date, ads, amicell_mA, amicell_v, amicell_% > $LOG_FILE

while [ condition ]
do
   now=`date`
   ads=`python3 get_v.py |grep adj |cut -d' ' -f2`
   amicell_mA=`python3 get_battery_level.py |grep 2020 |cut -d',' -f3`
   amicell_v=`python3 get_battery_level.py |grep 2020 |cut -d',' -f4`
   percent=`python3 get_battery_level.py |grep 2020 |cut -d',' -f6`
   echo $now,$ads,$amicell_mA,$amicell_v,$percent >> $LOG_FILE
   sleep 30
done
