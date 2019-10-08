import os, glob, numpy as np
from mcni.utils import conversion

elements_weight_percentage_gasket= {'C':0.15, 'Mn':2.00, 'P':0.045, 'S':0.03, 'Cr':16.0, 'Ni':6, 'N':0.10, 'Fe':75.67}

elements_weight_percentage_seat = {'C':0.03, 'Mn':0.10, 'P':.01, 'S':0.01, 'Si':0.10, 'Ni':18.5, 'Mo':4.8, 'Co':12.00,
                 'Ti':1.40, 'Al':0.10, 'B':0.003, 'Zr':0.01, 'Fe':62.83}

Avogrados_number = 6.023e23

atomic_weight = {'C':12, 'Mn':54.9, 'P':30.9, 'S':32.06, 'Cr':51.9, 'Ni':58.6, 'N':14.0, 'Fe':55.8,
                 'Si':28.08, 'Mo':95.9, 'Co':28.01, 'Ti':47.8, 'Al':26.9, 'B':10.81 ,'Zr':91.2}



# elements_number_of_atoms_gasket = [(k,elements_weight_percentage_gasket[k]*
#                                    Avogrados_number/atomic_weight[k])for k in
#                                    elements_weight_percentage_gasket.keys()]
elements_number_of_atoms_gasket= {}
elements_number_of_atoms_seat= {}

def atomic_percentage_from_weight_percentage(weight_percentage, atomic_weight ):
    number_of_atoms = {}
    atomic_percentage = {}
    for k in weight_percentage.keys():
        number_of_atoms[k] = weight_percentage[k]*Avogrados_number/atomic_weight[k]

    total_number_atoms= sum(number_of_atoms.values())
    for k in weight_percentage.keys():
        atomic_percentage[k] = number_of_atoms[k]*100./total_number_atoms

    return (atomic_percentage)


elements_atomic_percentage_gasket = atomic_percentage_from_weight_percentage(
                                           elements_weight_percentage_gasket,
                                           atomic_weight)

elements_atomic_percentage_seat = atomic_percentage_from_weight_percentage(
                                           elements_weight_percentage_seat,
                                           atomic_weight)

print (elements_atomic_percentage_gasket, elements_atomic_percentage_seat)


















