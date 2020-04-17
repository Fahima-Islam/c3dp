import numpy as np
from braggedgemodeling import bem

def d_hkl(scatterer):
    scat = bem.matter.loadCif('{}.cif'.format(scatterer))
    material = scat
    xsc = bem.xscalc.XSCalculator(material, 300)

    peaks = xsc.diffpeaks

    d=[p.d for p in peaks[5:6]]
    hkl=[p.hkl for p in peaks]
    F=[p.F for p in peaks ]
    d=np.hstack(d)
    F = np.hstack(F)
    # hkl=np.hstack(hkl)

    return (d,hkl,F)

si_d, si_hkl, I_si= d_hkl('/home/fi0/Instrument_optimization/CIF_file_CLAMPCELL/Al')
print (si_d)
# si_d, si_hkl= d_hkl('/home/fi0/Instrument_optimization/CIF_file_CLAMPCELL/Si')
#
# print (si_hkl[0])
