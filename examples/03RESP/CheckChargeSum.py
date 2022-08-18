#! /usr/bin/env python3
# -*- Coding: UTF-8 -*-

import decimal
import sys

if len(sys.argv) > 1:
    iname = sys.argv[1]
else:
    print("This program checks the sum of charges in a chg file.")
    print("Input file name:")
    iname = input()
if not iname.endswith(".chg"):
    print("Warning: adding \".chg\" suffix for input name.")
    iname += ".chg"

tot = decimal.Decimal('0')
with open(iname) as f:
    for l in f:
        s = l.strip()
        if not s: break
        t = s.split()
        tot += decimal.Decimal(t[4])

print('The sum of charges is:', tot)

