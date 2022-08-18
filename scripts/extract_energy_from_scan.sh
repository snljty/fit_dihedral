#! /bin/bash

grep -v '^#' scan_tot_ener.txt | awk '{printf "%17.10f\n",$2}' > qm_scan_energy.txt

