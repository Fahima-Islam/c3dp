from c3dp.reduction.from_d_toTOF import tof_from_d
import numpy as np

import pytest

@pytest.mark.parametrize('d, angle, l1, '
                         'l2, l3, xA,yA, zA, expected_value', [(3.12, 55, 14.699, 0.3,0.5,0.0,0.0,0.0, 11.299)])
def test_tof_from_d(d,angle, l1, l2, l3, xA,yA, zA, expected_value ):
    np.testing.assert_allclose(tof_from_d(d, angle, l1=l1, l2=l2, l3=l3, xA=xA, yA=yA, zA=zA), expected_value, atol=0.01)

