#! /bin/bash

natoms=`head -n 1 isomers.xyz | awk '{print $1}'`
nlines=`expr ${natoms} + 2`
sed -n "2~${nlines}p" isomers.xyz | awk '{print $3}' > qm_scan_energy.txt

