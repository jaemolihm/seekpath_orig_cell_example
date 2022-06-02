#!/usr/bin/env python3
import numpy as np
import seekpath

cell = [[-0.5, 0.0, 0.5], [0.0, 0.5, 0.5], [-0.5, 0.5, 0.0]]
positions = [[0.0, 0.0, 0.0], [0.25, 0.25, 0.25]]
atomic_numbers = [0, 0]

s = np.sin(0.1)
c = np.cos(0.1)
R = np.array([[c, s, 0.], [-s, c, 0.], [0., 0., 1.]])

T = np.array([[1, 0, 0], [0, 1, 0], [1, 0, 1]])

cell = T @ cell @ R
positions = positions @ np.linalg.inv(T)
structure = (cell, positions, atomic_numbers)

res_standard = seekpath.get_explicit_k_path(structure, reference_distance=0.3)
res_original = seekpath.get_explicit_k_path_orig_cell(structure, reference_distance=0.3)

print("=" * 40)
print("Standard unit cell:")
for i in range(3):
    print(f"a({i+1}) = ", res_standard["primitive_lattice"][i])
print("Standard atomic positions:")
for i in range(len(res_standard["primitive_positions"])):
    print(f"tau({i+1}) = ", res_standard["primitive_positions"][i])

print("k points for the standard cell:")
print("K_POINTS crystal")
print(len(res_standard["explicit_kpoints_rel"]))
for k in res_standard["explicit_kpoints_rel"]:
    print(f"{k[0]:12.8f}{k[1]:12.8f}{k[2]:12.8f} 1.0")

print("=" * 40)
print("Non-standard unit cell:")
for i in range(3):
    print(f"a({i+1}) = ", cell[i])
print("Non-standard atomic positions:")
for i in range(len(res_standard["primitive_positions"])):
    print(f"tau({i+1}) = ", positions[i])

print("k points for the non-standard cell:")
print("K_POINTS crystal")
print(len(res_original["explicit_kpoints_rel"]))
for k in res_original["explicit_kpoints_rel"]:
    print(f"{k[0]:12.8f}{k[1]:12.8f}{k[2]:12.8f} 1.0")


cell_supercell = [cell[0], cell[1], [2 * x for x in cell[2]]]
positions_supercell = ([x / np.array([1, 1, 2]) for x in positions]
                     + [x / np.array([1, 1, 2]) + np.array([0, 0, 0.5]) for x in positions])
atomic_numbers_supercell = atomic_numbers + atomic_numbers
structure_supercell = (cell_supercell, positions_supercell, atomic_numbers_supercell)

res_supercell = seekpath.get_explicit_k_path_orig_cell(structure_supercell, reference_distance=0.3)

print("=" * 40)
print("Supercell:")
for i in range(3):
    print(f"a({i+1}) = ", cell_supercell[i])
print("Super atomic positions:")
for i in range(len(positions_supercell)):
    print(f"tau({i+1}) = ", positions_supercell[i])

print("k points for the supercell:")
print("K_POINTS crystal")
print(len(res_supercell["explicit_kpoints_rel"]))
for k in res_supercell["explicit_kpoints_rel"]:
    print(f"{k[0]:12.8f}{k[1]:12.8f}{k[2]:12.8f} 1.0")
