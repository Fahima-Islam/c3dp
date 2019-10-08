import numpy as np
from scipy.integrate import trapz, simps


def area_under_curve(y, dx, method=None):
    if method == "trapz":
        area = np.trapz(y, dx=dx)

    if method == 'simps':
        area = simps(y, dx=dx)

    if method == 'my_code':
        i = 1
        total = y[0] + y[-1]
        for y_vals in y[1:-1]:
            if i % 2 == 0:
                total += 2 * y_vals
            else:
                total += 4 * y_vals
            i += 1
        area =  total * (dx / 3.0)

    return (area)


def normalization (y, area):

    return(y/area)

