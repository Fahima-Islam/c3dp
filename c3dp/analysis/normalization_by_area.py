import numpy as np
from scipy.integrate import  simps


def area_under_curve(y, dx, method=None):
    """Calculate the area under the curve


       Parameters
       ----------
       y: array_like
            Input array to integrate

        dx : scalar
            The spacing between sample points

       Returns
       -------
       area: float
           Integrated area
       """
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
    """normalizing the curve by integrated area


        Parameters
        ----------
        y: array_like
             Input array to integrate

         area: float
           Integrated area

        Returns
        -------
        normalized_data:array_like
             normalized curve by area

        """

    return(y/area)

