import numpy as np, os, sys
sys.path.insert(0,'/home/fi0/dev/SNAP/SNAP_2018_package/braggedgemodeling/')
import bem
from bem import xscalc


def d_hkl(scatterer):
    scat = bem.matter.loadCif('{}.cif'.format(scatterer))
    material = scat
    xsc = xscalc.XSCalculator(material, 300)

    peaks = xsc.diffpeaks

    d=[p.d for p in peaks]
    hkl=[p.hkl for p in peaks]
    F=[p.F for p in peaks ]
    d=np.hstack(d)
    F = np.hstack(F)
    # hkl=np.hstack(hkl)

    return (d,hkl,F)

si_d, si_hkl, I_si= d_hkl('/home/fi0/Instrument_optimization/CIF_file_CLAMPCELL/Si')
# si_d, si_hkl= d_hkl('/home/fi0/Instrument_optimization/CIF_file_CLAMPCELL/Si')
#
# print (si_hkl[0])
