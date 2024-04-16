#! /usr/bin/env python3
# -*- Coding: UTF-8 -*-

import os
import numpy as np
import matplotlib.pyplot as plt

plt.rc("font", size = 14)

start_value = -1.10287 # the start dihedral
num_scan = 18
step_value = 10.0
x = np.arange(num_scan + 1).astype(np.float64) * step_value + start_value
x = (x + 180.0) % 360 - 180.0

num_dims = 3

# auxiliary
def Get_vector_angle(p: np.double, q: np.double) -> np.double:
    # p, q are vectors, return in unit degree
    assert p.dtype == np.double and q.dtype == np.double
    assert p.shape == (num_dims,) and q.shape == (num_dims,)
    return np.degrees(np.arccos(np.dot(p, q) / (np.linalg.norm(p) * np.linalg.norm(q))))

# length
def Get_distance(a: np.double, b: np.double) -> np.double:
    # a, b are points
    assert a.dtype == np.double and b.dtype == np.double
    assert a.shape == (num_dims,) and b.shape == (num_dims,)
    return np.linalg.norm(b - a)

# angle
def Get_angle(a: np.double, b: np.double, c: np.double) -> np.double:
    # a, b, c are points, return in unit degree
    assert a.dtype == np.double and b.dtype == np.double and c.dtype == np.double
    assert a.shape == (num_dims,) and b.shape == (num_dims,) and c.shape == (num_dims,)
    return Get_vector_angle(b - a, b - c)

# dihedral
def Get_dihedral(a: np.double, b: np.double, c: np.double, d: np.double) -> np.double:
    # a, b, c, d are points, return in unit degree
    assert a.dtype == np.double and b.dtype == np.double and c.dtype == np.double and d.dtype == np.double
    assert a.shape == (num_dims,) and b.shape == (num_dims,) and c.shape == (num_dims,) and d.shape == (num_dims,)
    p = np.cross(b - a, b - c)
    q = np.cross(c - d, b - c)
    return Get_vector_angle(p, q) * (-1.0 if np.dot(p, c - d) < 0.0 else 1.0)

if os.path.isfile("traj.xyz"):
    if os.path.isfile("dihedral.txt"):
        with open("dihedral.txt") as ifl:
            atom1, atom2, atom3, atom4 = map(int, ifl.readline().split())
    else:
        ifl_names = [_ for _ in os.listdir() if os.path.isfile(_) and _.endswith(".out")]
        if len(ifl_names) == 1:
            with open(* ifl_names) as ifl:
                for line in ifl:
                    if "The following ModRedundant input section has been read:" in line:
                        break
                line = ifl.readline().split()
                assert line[0] == "D" and line[5] == "S"
                atom1, atom2, atom3, atom4 = map(int, line[1:5])
        else:
            ifl_names = [_ for _ in os.listdir() if os.path.isfile(_) and _.endswith(".gjf")]
            if len(ifl_names) == 1:
                with open(* ifl_names) as ifl:
                    line = ifl.readlines()[-2].split()
                    if line[0] != "D":
                        line.insert(0, "D")
                    assert line[5] == "S"
                    atom1, atom2, atom3, atom4 = map(int, line[1:5])
if "atom1" in dir():
    num_scan = -1
    with open("traj.xyz") as ifl:
        num_atoms = int(ifl.readline())
    element_names = ["" for _ in range(num_atoms)]
    coordinates = []
    x = []
    with open("traj.xyz") as ifl:
        while True:
            line = ifl.readline()
            if not line: break
            assert int(line) == num_atoms
            ifl.readline()
            num_scan += 1
            coordinates.append(np.zeros((num_atoms, num_dims), dtype = np.double))
            for i in range(num_atoms):
                line = ifl.readline().split()
                if element_names[i]:
                    assert line[0] == element_names[i]
                else:
                    element_names[i] = line[0]
                coordinates[num_scan][i, :] = np.array(line[1:], dtype = np.double)
            x.append(Get_dihedral(coordinates[num_scan][atom1 - 1, :], \
                                  coordinates[num_scan][atom2 - 1, :], \
                                  coordinates[num_scan][atom3 - 1, :], \
                                  coordinates[num_scan][atom4 - 1, :]))
    x = np.array(x, dtype = np.double)
else:
    print("Note: using dihedrals set in this script ({:s}).".format(sys.argv[0]))

title = "structure"
x_label = u"dihedral (\u00b0)"

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
ax.set_xticks(np.linspace(-180.0, 180.0, 9))
# ax.set_xticks(np.linspace(0.0, 180.0, 7))
ax.set_xlabel(x_label)
ax.set_ylabel("Relative energy (kJ/mol)")
ax.set_title(title)

y_diff = y_qm - y_mm
np.savetxt("energy_diff.txt", np.array([x, y_diff]).T, fmt = ["%6.1f", "%10.4f"], delimiter = " " * 14, header = "dihedral(degree)     energy(kJ/mol)")

fig.savefig("compare_scan_qm_mm.png")
if os.name == "nt" or os.getenv("DISPLAY"):
    plt.show()

