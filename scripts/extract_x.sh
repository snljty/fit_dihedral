#! /bin/bash -e

if [[ -z $1 ]]
then
    echo -n 'Input output name of Gaussian relaxed scan task: '
    read outname
else
    outname=$1
fi

# natoms=`grep -m 1 'NAtoms=' $outname | awk '{print int($2)}'`
nline_beg=`grep -n 'Initial Parameters' $outname | awk -F ':' '{print 5+int($1)}'`
x_label=`tail -n "+$nline_beg" $outname | grep -m 1 'Scan' | awk '{print $3}'`
grep "$x_label" $outname | tail -n +2 | awk '{printf "%9.4f\n", $4}' > x.txt

