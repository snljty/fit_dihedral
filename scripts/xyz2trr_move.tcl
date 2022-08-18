#! /bin/tclsh
mol new traj.xyz type xyz
set bsize 102.3
set mvlen [expr $bsize / 2]
set sel [atomselect top all]
set nframes [molinfo top get numframes]
for {set i 0} {$i < $nframes} {incr i} {
    animate goto $i
    $sel moveby "$mvlen $mvlen $mvlen"
}
pbc set "$bsize $bsize $bsize" -all
# mol modstyle 0 top CPK 1.0 0.3 25 25
# pbc box -on -color white
animate write trr traj.trr
exit
