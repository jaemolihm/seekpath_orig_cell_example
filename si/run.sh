#!/bin/bash
set -ex

mpirun -np 4 pw.x -nk 4 -in scf.standard.in > scf.standard.out
mpirun -np 4 pw.x -nk 4 -in bands.standard.in > bands.standard.out

mpirun -np 4 pw.x -nk 4 -in scf.nonstandard.in > scf.nonstandard.out
mpirun -np 4 pw.x -nk 4 -in bands.nonstandard.in > bands.nonstandard.out

srun -n 40 --partition=G3 pw.x -nk 10 -in scf.supercell.in > scf.supercell.out
srun -n 40 --partition=G3 pw.x -nk 10 -in bands.supercell.in > bands.supercell.out