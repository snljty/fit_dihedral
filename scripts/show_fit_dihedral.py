#! /usr/bin/env python3
# -*- Coding: UTF-8 -*-

import numpy as np
import matplotlib.pyplot as plt
import os

# plt.rc("font", size = 14)

k = [0.,]
with open("fit_result.txt") as f:
    while True:
        line = f.readline().strip()
        if not line:
            break
        if line[0] == "k":
            k.append(np.double(line.split("=")[1]))
        elif line.startswith("phase"):
            k = np.array(k)
            phase = np.double(line.split("=")[1])

x = np.linspace(-180.0, 180.0, 361)

y = [np.zeros(x.size)]
y_min = 0.0
y_max = 0.0
for i in np.arange(1, k.size):
    y.append(y[-1] + k[i] * (1 + np.cos(np.radians(i * x - phase))))
    # y[-1] -= y[-1].mean()
    y_min = min(y_min, y[-1].min())
    y_max = max(y_min, y[-1].max())
for i in np.arange(1, k.size):
    y[i] -= y[i].min()
y_max -= y_min
y_min = 0

fig, ax = plt.subplots()
for i in np.arange(1, k.size):
    ax.plot(x, y[i], color = "#%02X00%02X" % ( \
        int(np.round(((i - 1) / (k.size - 2) * 0xFF))), 0xFF - int(np.round(((i - 1) / (k.size - 2) * 0xFF))) \
        ), label = (("%d terms" % i) if i != 1 else ("%d term" % i)))
    # ax.plot(x, y[i], label = "%d terms" % i)
ax.legend()
ax.set_xticks(np.linspace(-180.0, 180.0, 9))
ax.set_xlabel(u"Dihedral (\u00b0)")
ax.set_ylabel("Relative energy (kJ/mol)")
ax.set_title("Different Amount of Terms Of Fitting")
# y_lim_min = np.floor(y_min / 10) * 10
y_lim_min = 0
y_lim_max = np.ceil(y_max / 10) * 10
# ax.set_ylim(y_lim_min, y_lim_max)
ax.set_yticks(np.linspace(y_lim_min, y_lim_max, int(np.round((y_lim_max - y_lim_min) / 10 + 1))))

fig.savefig("Different_amount_of_terms_of_fitting.png")
if os.name == "nt" or os.getenv("DISPLAY"):
    plt.show()

