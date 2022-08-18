#! /usr/bin/env python3
# -*- Coding: UTF-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rc("font", size = 14)

start_value = 26.56736 # the start dihedral
num_scan = 36
step_value = 10.0

title = "structure"
x_label = u"dihedral (\u00b0)"

x = np.arange(num_scan + 1).astype(np.float64) * step_value + start_value
x = (x + 180.0) % 360 - 180.0

y_qm = np.loadtxt("qm_scan_energy.txt", unpack = True)
y_mm = np.loadtxt("mm_potential.xvg", comments = ["#", "@"], unpack = True, usecols = 1)

sort_seq = np.argsort(x)
np.savetxt("x_sort_seq.txt", sort_seq, fmt = "%2d")
y_qm = y_qm[sort_seq]
y_mm = y_mm[sort_seq]
x = x[sort_seq]

min_pos = np.argmin(y_qm)
y_qm -= y_qm[min_pos]
y_qm *= 2625.499 # convert from Hartree to kJ/mol
y_mm -= y_mm[min_pos]

fig, ax = plt.subplots()

ax.plot(x, y_qm, color = "red", marker = "o", markersize = 5, label = "QM")
ax.plot(x, y_mm, color = "blue", marker = "o", markersize = 5, label = "MM")
ax.legend()
ax.set_xticks(np.linspace(-180.0, 180.0, num_scan // 3 + 1))
# ax.set_xticks(np.linspace(0.0, 180.0, num_scan // 3 + 1))
ax.set_xlabel(x_label)
ax.set_ylabel("Relative energy (kJ/mol)")
ax.set_title(title)

y_diff = y_qm - y_mm
np.savetxt("energy_diff.txt", np.array([x, y_diff]).T, fmt = ["%6.1f", "%10.4f"], delimiter = " " * 14, header = "dihedral(degree)     energy(kJ/mol)")

fig.savefig("compare_scan_qm_mm.png")
if os.name == "nt" or os.getenv("DISPLAY"):
    plt.show()

