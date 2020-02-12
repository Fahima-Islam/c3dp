from instrument.atomicPercentage_from_weightPencentage import atomic_percentage_from_weight_percentage as apw
import pytest
import numpy as np
from collections import OrderedDict

@pytest.mark.parametrize('elements_weight_percentage_gasket, elements_weight_percentage_seat, atomic_weight, '
                         'target_elements_atomic_percentage_gasket, ',
                         [({'C':0.15, 'Mn':2.00, 'P':0.045, 'S':0.03, 'Cr':16.0, 'Ni':6, 'N':0.10, 'Fe':75.67},
                           {'C':0.03, 'Mn':0.10, 'P':.01, 'S':0.01, 'Si':0.10, 'Ni':18.5, 'Mo':4.8, 'Co':12.00,
                     'Ti':1.40, 'Al':0.10, 'B':0.003, 'Zr':0.01, 'Fe':62.83},
                           {'C':12, 'Mn':54.9, 'P':30.9, 'S':32.06, 'Cr':51.9, 'Ni':58.6, 'N':14.0, 'Fe':55.8,
                     'Si':28.08, 'Mo':95.9, 'Co':28.01, 'Ti':47.8, 'Al':26.9, 'B':10.81 ,'Zr':91.2},
                           OrderedDict(
                               [('S', 0.05126720139961481), ('Fe', 74.29702240434757), ('P', 0.0797876930520219),
                                ('Ni', 5.609646678742836), ('Cr', 16.89018858699192), ('Mn', 1.99590343275246),
                                ('N', 0.39133963735039307), ('C', 0.6848443653631879)])

                           )])

def test_atomic_percentage_from_weight_percentage(elements_weight_percentage_gasket,elements_weight_percentage_seat,
                                                  atomic_weight, target_elements_atomic_percentage_gasket):

    elements_atomic_percentage_gasket = apw(elements_weight_percentage_gasket, atomic_weight)
    elements_atomic_percentage_seat = apw(elements_weight_percentage_seat, atomic_weight)
    np.testing.assert_allclose(elements_atomic_percentage_gasket, target_elements_atomic_percentage_gasket, atol=0.01)

