#! /usr/bin/env python3
# coding: utf-8

import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
y, y1, y2 = np.loadtxt("angaver.xvg", unpack = True, usecols = [1, 2, 3], comments = ["#", "@"])

ax.hist(y, bins = 100, color = "black")
ax.set_xticks(np.linspace(- 180, 180, 9))

fig.savefig("dih_dist.png")

plt.show()

