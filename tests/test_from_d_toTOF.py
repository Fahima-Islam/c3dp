from c3dp.reduction.from_d_toTOF import tof_from_d
import numpy as np

import pytest

@pytest.mark.parametrize('d, angle, l1, '
                         'l2, l3, xA,yA, zA, expected_value', [(3.12, 55, 14.699, 0.3,0.5,0.0,0.0,0.0, 11.299)])
def test_tof_from_d(d,angle, l1, l2, l3, xA,yA, zA, expected_value ):
    """
    conversion to time of flight to d spacing

    Parameters
    ----------
   d : float
        d spacing in Angstrom.
    angle : float
        scattering angles in degrees.
    l1 : float
        from source to guide exit distance in meters
    l2 : float
        from guide to sample distance in meters
    l3 : float
        from sample to detector distance in meters
    xA : float
        pixel position along x-axis with respect to detector center in meters
    yA : float
        pixel position along y-axis with respect to detector center in meters
    zA : float
        pixel position along z-axis with respect to detector center in meters
    expected_value: float
        expected value of time of flight

    Returns
    -------

    """
    np.testing.assert_allclose(tof_from_d(d, angle, l1=l1, l2=l2, l3=l3, xA=xA, yA=yA, zA=zA), expected_value, atol=0.01)

