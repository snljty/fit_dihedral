#! /usr/bin/env python3
# -*- Coding: UTF-8 -*-

r"""
Calculate the RESP2 charge using charge of voccum and solute.
Usage: python RESP2.py SP_gas.chg SP_solv.chg [ 0.5 ]
"""

from sys import argv
argc = len(argv)

delta = 0.5
if argc >= 4: delta = float(argv[3])
if argc >= 3:
    fn_gas = argv[1]
    fn_solv = argv[2]
else:
    fn_gas = input("Input the file name fo SP_gas.chg:\n")
    fn_solv = input("Input the file name fo SP_solv.chg:\n")
    temp = input("Directly press ENTER to use the default value: 0.5\nInput the delta value: ")
    if (not temp.isspace()) and (temp != str()): delta = float(temp)
with open(fn_gas) as f_gas, open(fn_solv) as f_solv, open("RESP2_result.chg", "w") as f_res:
    while True:
        temp = f_gas.readline()
        if (temp.isspace()) or (temp == str()): break
        vals = temp.strip().split()
        c_gas = float(vals[4])
        c_solv = float(f_solv.readline().strip().split()[4])
        print("%-2s  %10.6lf  %10.6lf  %10.6lf  %13.10lf"
              % (vals[0], float(vals[1]), float(vals[2]), float(vals[3]),
                 (1 - delta) * c_gas + delta * c_solv), file = f_res)
print("Done. Result has been saved to \"RESP2_result.chg\".")
        
