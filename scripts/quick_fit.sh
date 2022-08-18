#! /bin/bash -e

# do not remove the '-e' option in the first line (intepreater)

potterm=9 # the number of potential energy term of gmx energy in this situation
numtermfit=8 # number of terms in the fitting expression

grofile=`ls -1 *.gro | head -1` # may need to spicify yourself
groname=${grofile%\.*}
topfile=`ls -1 *.top`
topname=${topfile%\.*}

[[ -e ${grofile} ]]
echo "Found ${grofile}"
[[ -e ${topfile} ]]
echo "Found ${topfile}"
[[ -e scan.mdp ]]
echo 'Found scan.mdp'
[[ -e traj.trr ]]
echo 'Found traj.trr'
[[ -e draw_compare_qm_mm.py ]]
echo 'Found draw_compare_qm_mm.py'
[[ -e prepare_fit_dih_py.sh ]]
echo 'Found prepare_fit_dih_py.sh'
[[ -e fit_dih_template.py ]]
echo 'Found fit_dih_template.py'
[[ -e qm_scan_energy.txt ]]
echo 'Found qm_scan_energy.txt'
echo '####################################################'
echo '# Don'"'"'t forget to modify draw_compare_qm_mm.py !!! #'
echo '####################################################'

gmx grompp -f scan.mdp -c ${groname}.gro -p ${topname}.top -o scan.tpr -nobackup
gmx mdrun -nt 1 -v -deffnm scan -rerun traj.trr -nobackup
echo ${potterm} 0 | gmx energy -f scan.edr -o mm_potential.xvg -nobackup
read -p 'Press <Enter> to continue'
python draw_compare_qm_mm.py
./prepare_fit_dih_py.sh ${numtermfit}
python fit_dih.py
echo 'Now modify the itp file.'

