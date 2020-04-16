from c3dp.instruments.atomicPercentage_from_weightPencentage import atomic_percentage_from_weight_percentage as apw
import pytest
import numpy as np
from collections import OrderedDict


@pytest.mark.parametrize('elements_weight_percentage_gasket, elements_weight_percentage_seat, atomic_weight, '
                         'target_elements_atomic_percentage_gasket, target_elements_atomic_percentage_seat ',
                         [(
                           OrderedDict(
                               [('S', 0.03), ('Fe', 75.67), ('P', 0.045),
                                ('Ni', 6), ('Cr', 16.0), ('Mn', 2.00),
                                ('N', 0.10), ('C', 0.15)]),
                           OrderedDict(
                               [('S', 0.01), ('Fe', 62.83), ('P', .01),
                                ('Ni', 18.5), ('Mn', 0.10),
                                ('C', 0.03), ('Zr', 0.01), ('B', 0.003), ('Al', 0.10),
                                ('Ti', 1.40), ('Co', 12.00), ('Mo', 4.8), ('Si', 0.10)]),

                           OrderedDict(
                               [('S', 32.06), ('Fe', 55.8), ('P', 30.9),
                                ('Ni', 58.6), ('Cr', 51.9), ('Mn', 54.9),
                                ('N', 14.0), ('C', 12), ('Zr', 91.2), ('B', 10.81), ('Al', 26.9),
                                ('Ti', 47.8), ('Co', 28.01), ('Mo', 95.9), ('Si', 28.08)]),

                           OrderedDict(
                               [('S', 0.051), ('Fe', 74.297), ('P', 0.079),
                                ('Ni', 5.609), ('Cr', 16.890), ('Mn', 1.995),
                                ('N', 0.391), ('C', 0.684)]),

                           OrderedDict([('S', 0.0158), ('Fe', 57.387),
                                        ('P', 0.016), ('Ni', 16.090),
                                        ('Mn', 0.092), ('C', 0.127),
                                        ('Zr', 0.005), ('B', 0.014),
                                        ('Al', 0.189), ('Ti', 1.49),
                                        ('Co', 21.835), ('Mo', 2.550),
                                        ('Si', 0.181)])

                           )])
def test_atomic_percentage_from_weight_percentage(elements_weight_percentage_gasket, elements_weight_percentage_seat,
                                                  atomic_weight, target_elements_atomic_percentage_gasket,
                                                  target_elements_atomic_percentage_seat):
    """
    testing atomic percentage from weight percentage function

    Parameters
    ----------
    elements_weight_percentage_gasket:ordered dictionary
        elements as keys and their weight percentage as values in gasket of DAC
    elements_weight_percentage_seat:ordered dictionary
        elements as keys and their weight percentage as values in seat of DAC
    atomic_weight: ordered dictionary
        elements as keys and their atomic weights as values
    target_elements_atomic_percentage_gasket: ordered dictionary
        elements as keys and their atomic percentage as values in gasket
    target_elements_atomic_percentage_seat: ordered dictionary
        elements as keys and their atomic percentage as values in seat

    Returns
    -------

    """

    elements_atomic_percentage_gasket = apw(elements_weight_percentage_gasket, atomic_weight)
    elements_atomic_percentage_seat = apw(elements_weight_percentage_seat, atomic_weight)
    np.testing.assert_allclose(list(elements_atomic_percentage_gasket.values()),
                               list(target_elements_atomic_percentage_gasket.values()), atol=0.01)
    np.testing.assert_allclose(list(elements_atomic_percentage_seat.values()),
                               list(target_elements_atomic_percentage_seat.values()), atol=0.01)
