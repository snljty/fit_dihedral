#!/usr/bin/env python3
# coding: utf-8

import sys
import numpy as np
import matplotlib.pyplot as plt

angle, qm = np.loadtxt("QM.txt", unpack=True)
t, mm = np.loadtxt("MM.xvg", unpack=True, comments=["#", "@"])
qm -= qm[0]
qm *= 2625.5
mm -= mm[0]

fig, ax = plt.subplots()

ax.plot(angle, qm, marker="o", label="QM", color="red")
ax.plot(angle, mm, marker="o", label="MM", color="blue")
ax.set_xticks(np.linspace(angle[0], angle[-1], 7))
ax.set_xlabel("Dihedral (\u00B0)")
ax.set_ylabel("Relative energy (kJ/mol)")
y_axis_lower = min(qm.min(), mm.min())
y_axis_upper = max(qm.max(), mm.max())
y_axis_lower = np.floor(y_axis_lower / 10.) * 10.
y_axis_upper = np.ceil(y_axis_upper / 10.) * 10.
ax.set_yticks(np.arange(y_axis_lower, y_axis_upper + 1., 10.))
ax.set_title("Difference of QM and MM")
ax.legend()

# fig.savefig("compare.png")
# fig.savefig("compare.svg")

plt.show()
