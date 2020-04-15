import numpy as np
Mn=1.67e-27 #Mass of Neutrons (kg)
h=6.60e-34 #Planck's const (Js)

CF=(h*1e7)/Mn #(3.952) time should be in milisecond and wavelength should be in angstrom

def tof_from_d( d, angle, l1=14.699, l2=0.3, l3=0.5, xA=0.0, yA=0.0,zA=0.0):

    r"""
     unit conversion from d spacing to time of flight
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

    Returns
    -------
    time of flight in seconds

     """

    L = l1 + l2 + np.sqrt(xA ** 2 + yA ** 2 + (zA + l3) ** 2)
    angle = np.deg2rad(angle*1.)
    m = np.array([
        [np.cos(angle), 0, np.sin(angle)],
        [0, 1, 0],
        [-np.sin(angle), 0, np.cos(angle)]
        ])
    labCoords = np.dot(m, np.array([xA, yA, zA])).T + [l3*np.sin(angle), 0, l3*np.cos(angle)]
    # print labCoords[2]
    cos2theta = labCoords[2]/np.linalg.norm(labCoords, axis=-1)
    sintheta = np.sqrt((1 - cos2theta) / 2)
    # twotheta = np.arccos(cos2theta) * 180./np.pi
    lamda=d*(2 * sintheta)
    tof=lamda* L/CF

    return tof




