#POSCAR set unite cell 
import numpy as np
import os
import ase.io as o
from ase import Atoms
atoms = o.read('POSCAR0')
'''
print(atoms.get_positions()) # Cartisian
print(atoms.get_scaled_positions()) #Frac
print(atoms.cell)
cell_Mtx=atoms.cell[:] #array of unit cell
print(cell_Mtx)
a=cell_Mtx[0][0]
print(a)
b=cell_Mtx[1][1]
print(b)
c=cell_Mtx[2][2]
print(c)
'''
ept_list=np.arange(0.8,1.2,0.1) #strain arange
for x in ept_list:
    atoms.set_cell([[x*5. ,0. ,      0.      ], [0. ,  x*5.622697 ,0.      ], [0. ,  0.    ,   7.453415]],scale_atoms=True)# set new unite cell with scaled atoms
    os.makedirs('./%s/'%x)
    o.write('./%s/POSCAR'%x,atoms, vasp5=True, sort=True)
    print(atoms.cell)