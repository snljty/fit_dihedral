#!/usr/bin/env python3
# coding: utf-8

import sys
import numpy as np
import matplotlib.pyplot as plt

n: int = 8
if len(sys.argv) - 1 != 0:
    n = int(sys.argv[1])

phase: np.double = 0.

angle, qm = np.loadtxt("QM.txt", unpack=True)
t, mm = np.loadtxt("MM.xvg", unpack=True, comments=["#", "@"])
qm -= qm[0]
qm *= 2625.5
mm -= mm[0]

y = qm - mm # intrinsic
angle_rad = np.radians(angle)

X = np.zeros((len(mm), n + 1), dtype=np.double)
for i in range(1, 1 + n):
    X[:, i] = np.cos(i * angle_rad)
X[:, 0] = 1.

k = np.linalg.solve(X.T @ X, X.T @ y)
k[0] = - sum(k[1:])

with open("fit_result.txt", "w") as ofile:
    print("# phase        kd        pn")
    print("# phase        kd        pn", file=ofile)
    for i in range(1 + n):
        print(f"{phase:6.1f}     {k[i]:10.6f}    {i:2d}")
        print(f"{phase:6.1f}     {k[i]:10.6f}    {i:2d}", file=ofile)

fit = 2. * k[0] + sum([k[i] * (1. + np.cos(i * angle_rad)) for i in range(1, 1 + n)])

mm_fitted = mm + fit

np.savetxt("fit_data.txt", np.vstack([angle, qm, mm_fitted, y]).T, fmt="%8.3f", delimiter="    ", 
    header="dihedral     QM          MM        Intrinsic")

fig, ax = plt.subplots()

ax.plot(angle, qm, marker="o", label="QM", color="red")
ax.plot(angle, mm_fitted, marker="o", label="MM", color="blue")
ax.plot(angle, y, label="intrinsic", color="green")
ax.set_xticks(np.linspace(angle[0], angle[-1], 7))
ax.set_xlabel("Dihedral (\u00B0)")
ax.set_ylabel("Relative energy (kJ/mol)")
y_axis_lower = min(qm.min(), mm_fitted.min(), y.min())
y_axis_upper = max(qm.max(), mm_fitted.max(), y.max())
y_axis_lower = np.floor(y_axis_lower / 10.) * 10.
y_axis_upper = np.ceil(y_axis_upper / 10.) * 10.
ax.set_yticks(np.arange(y_axis_lower, y_axis_upper + 1., 10.))
ax.set_title("Fit Result")
ax.legend()

# fig.savefig("fit_result.png")
# fig.savefig("fit_result.svg")

plt.show()
