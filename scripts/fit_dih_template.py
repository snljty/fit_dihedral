#! /usr/bin/env python3
# -*- Coding: UTF-8 -*-

import os, sys
import numpy as np
from scipy.optimize import curve_fit
# import matplotlib.pyplot as plt

title = "structure"
x_label = u"dihedral (\u00b0)"

x, y = np.loadtxt("energy_diff.txt", unpack = True, comments = "#")

def func(val, c, k1, k2, k3, k4, phase):
    k = [0, ] + [k1, k2, k3, k4]
    ret = c
    for i in np.arange(1, len(k)):
        ret += k[i] * (1 + np.cos(np.radians(i * val - phase)))
    return ret

p_opt, p_cov = curve_fit(func, x, y)
p_err = np.sqrt(np.diag(p_cov))
# print(p_err)
y_fit = list(map((lambda _: func(_, * p_opt)), x))
y_fit_diff = y_fit - y
np.savetxt("fit_diff.txt", y_fit_diff, fmt = "%12.7f")

# fig, ax = plt.subplots()
# ax.scatter(x, y, s = 16, c = "black")
# ax.plot(x, y_fit, color = "orange")
# ax.set_xticks(np.linspace(-180.0, 180.0, x.size // 3 + 1))
# ax.set_xlabel(x_label)
# ax.set_ylabel("Relative energy of dihedral (kJ/mol)")
# ax.set_title(title)
# ax.plot(x, y_fit - y, color = "purple")

# fig.savefig("fit_dih.png")
# plt.show()

with open ("fit_result.txt", "wt") as fl:
    for i in np.arange(1, len(p_opt) - 1):
        print("k[{i:2d}] = {k:10.6f}".format(i = i, k = p_opt[i]))
        print("k[{i:2d}] = {k:10.6f}".format(i = i, k = p_opt[i]), file = fl)
    print("phase = {phase:10.6f}".format(phase = p_opt[-1]))
    print("phase = {phase:10.6f}".format(phase = p_opt[-1]), file = fl)

if not os.path.exists("qm_scan_energy.txt") or not os.path.exists("mm_potential.xvg"):
    exit()

import matplotlib.pyplot as plt
plt.rc("font", size = 14)

print("", file = sys.stderr)
print('Will use data in "qm_scan_energy.txt", "mm_potential.xvg" and ', file = sys.stderr)
print('"x_sort_seq.txt" to test the effect of fitting ...', file = sys.stderr)
print('Please note that you need to guarantee that these files correspond to the "energy_diff.txt" file, ', file = sys.stderr)
print("and the mm_potential.xvg is from and rigid scan of force field WITHOUT the dihedral to be fitted.", file = sys.stderr)
y_qm = np.loadtxt("qm_scan_energy.txt")
y_mm_nodih = np.loadtxt("mm_potential.xvg", unpack = True, comments = ["#", "@"], usecols = 1)
x_sort_seq = np.loadtxt("x_sort_seq.txt", dtype = np.int64)
y_qm = y_qm[x_sort_seq]
y_mm_nodih = y_mm_nodih[x_sort_seq]
y_mm = y_mm_nodih + y_fit

min_pos = np.argmin(y_qm)
y_qm -= y_qm[min_pos]
y_qm *= 2625.499 # convert from Hartree to kJ/mol
y_mm -= y_mm[min_pos]

fig, ax = plt.subplots()

ax.plot(x, y_qm, color = "red", marker = "o", markersize = 5, label = "QM")
ax.plot(x, y_mm, color = "blue", marker = "o", markersize = 5, label = "MM")
ax.legend()
# ax.set_xticks(np.linspace(-180.0, 180.0, x.size // 3 + 1))
ax.set_xticks(np.linspace(0.0, 180.0, x.size // 3 + 1))
ax.set_xlabel(x_label)
ax.set_ylabel("Relative energy (kJ/mol)")
ax.set_title(title)

fig.savefig("compare_scan_qm_mm_fitted.png")
print('result has been saved to "compare_scan_qm_mm_fitted.png"', file = sys.stderr)
if os.name == "nt" or os.getenv("DISPLAY"):
    plt.show()

