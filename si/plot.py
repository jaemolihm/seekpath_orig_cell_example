#!/usr/bin/env python3
import numpy as np
import matplotlib.pyplot as plt
import seekpath

cell = [[-0.5, 0.0, 0.5], [0.0, 0.5, 0.5], [-0.5, 0.5, 0.0]]
positions = [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]
atomic_numbers = [0, 0]
structure = (cell, positions, atomic_numbers)
res = seekpath.get_explicit_k_path(structure, reference_distance=0.3)

xplot = res["explicit_kpoints_linearcoord"]
high_sym_x = []
high_sym_labels = []
for x, label in zip(xplot, res["explicit_kpoints_labels"]):
    if label != "":
        if len(high_sym_labels) > 0 and abs(x - high_sym_x[-1]) < 1e-10:
            high_sym_labels[-1] += "|" + label
        else:
            high_sym_x += [x]
            high_sym_labels += [label]
high_sym_labels = ["$\Gamma$" if x == "GAMMA" else x for x in high_sym_labels]


nbnd = 8
e_standard = np.loadtxt("si.standard.bands.dat.gnu").reshape((nbnd, -1, 2))[:, :, 1]
e_nonstandard = np.loadtxt("si.nonstandard.bands.dat.gnu").reshape((nbnd, -1, 2))[:, :, 1]
e_supercell = np.loadtxt("si.supercell.bands.dat.gnu").reshape((nbnd * 2, -1, 2))[:, :, 1]

for ib in range(nbnd):
    plt.plot(xplot, e_standard[ib], "k-", label="standard" if ib == 0 else None)
    plt.plot(xplot, e_nonstandard[ib], "r--", label="non-standard" if ib == 0 else None)
for ib in range(nbnd * 2):
    plt.plot(xplot, e_supercell[ib], "b-.", label="supercell" if ib == 0 else None)
for x in high_sym_x:
    plt.axvline(x, c="k", lw=1)
plt.xticks(high_sym_x, high_sym_labels)
plt.legend()
plt.xlim([min(xplot), max(xplot)])
plt.ylabel("energy (eV)")
plt.tight_layout()
plt.savefig("bands.png", dpi=300)
plt.show()