#! /bin/bash

if [[ -z $1 ]]
then
    echo 'Usage:' 1>&2
    echo "$0 num_k" 1>&2
    exit
else
    num_k=$1
fi

sed "s/k1, k2, k3, k4/`seq -f 'k%1.0f' -s ', ' $num_k`/" fit_dih_template.py > fit_dih.py
chmod +x fit_dih.py

