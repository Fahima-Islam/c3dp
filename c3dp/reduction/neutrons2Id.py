import  numpy as np
from mcni.utils import conversion
from mcni.neutron_storage import readneutrons_asnpyarr as rdn

def process(neutronspath):
    r"""
        calculating d spacing from the scattering events
       ----------
       neutronspath : str
           the path where the scattered neutron events are saved.

       Returns
       -------
       tuple
        Two float numbers:
        ``(d spacing in angstrom, probability of the scattered neutrons)``

        """

    narr = rdn(neutronspath)
    vx = narr[:,3]; vy = narr[:,4]; vz = narr[:,5]
    p = narr[:,9]
    v = (vx*vx + vy*vy +vz*vz)**.5
    cos2theta = vz/v
    lamda = 2 * np.pi / conversion.V2K / v
    sintheta = np.sqrt((1 - cos2theta) / 2)
    d = lamda / (2 * sintheta)
    return d, p
