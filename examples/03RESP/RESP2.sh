#! /bin/bash

delta=0.5

if [[ $# -gt 2 ]]
then
	echo "Error! Too many arguments! At most 2 required, but got $#." 1>&2
	exit 1
elif [[ $# -eq 2 ]]
then
	vac_fl=$1
	sol_fl=$2
elif [[ $# -eq 1 ]]
then
	echo "Error! You need to assign name for vacuum and solvated together." 1>&2
	exit 1
else
	read -p "Input name for vacuum: " vac_fl
	read -p "Input name for solvated: " sol_fl
fi

paste ${vac_fl} ${sol_fl} | awk '{printf ("%-3s %12.6f %12.6f %12.6f %15.10f\n",$1,$2,$3,$4,(1-d)*$5+d*$10)}' d=$delta > RESP2.chg

