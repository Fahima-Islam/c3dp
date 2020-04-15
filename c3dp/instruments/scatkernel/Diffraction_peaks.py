import numpy as np
from braggedgemodeling import bem

def _creating_configuration_file_for_temperature(temperature_file, significant_component, Temperature ):
    """
              creating the temperature configuration file

              Parameters
              ----------
              temperature_file: string
                 name of the temperature file with path
              significant_component: string
                    name of the xml geometry file to be saved
              Temperature: float
                    DebyeTemperatures

              """
    with open('{}.conf'.format(temperature_file), 'wt') as s:
        s.write('''DebyeTemperatures:
                    {significant_component}: {Temperature}'''.format(significant_component=significant_component,
                                                                     Temperature=Temperature))
def _q(lattice, h, k, l):
    """
    Returns q from (h, k, l) parameters
    Parameters
    ----------
    lattice: Lattice
    h: h
    k: k
    l: l

    Returns
    -------
    q: float

    """
    rb= lattice.recbase
    q = 2*np.pi*(h*rb[0] + k*rb[1] + l*rb[2])
    return np.sqrt(np.dot(q,q))

def diffraction(cif_file,temperature_file, samplefile_tosave_scatteringResult, significant_coponent,
                first_peak_index= 0, number_of_peaks=None, Temperatrure=300):
    """
              creating the diffraction peaks file

              Parameters
              ----------
              cif_file: string
                 cif file location of the scatterer
              temperature_file: string
                 name of the temperature file with path
              samplefile_tosave_scatteringResult: string
                  the directory of the scattering file with name to be saved
              significant_component: string
                    name of the xml geometry file to be saved
              number_of_peaks: int
                    number of diffraction peaks want to simulate
              Temperature: float
                    DebyeTemperatures

              """
    _creating_configuration_file_for_temperature(temperature_file, significant_coponent,Temperatrure )
    material =bem.matter.loadCif(cif_file)
    xsc = bem.xscalc.XSCalculator(material, Temperatrure)
    peaks = xsc.diffpeaks
    lattice = material.lattice
    lines_for_peaks = []
    qs = []
    if number_of_peaks is not None:
        last_peak_index = first_peak_index+number_of_peaks
        peaks = peaks [first_peak_index:last_peak_index]

    for p in peaks:
        F2 = np.abs(p.F)**2/100
        mul = p.mult
        h,k,l = p.hkl
        q = _q(lattice, h,k,l)
        qs.append(q)
        line = "Peak(q=%(q)s, F_squared=%(F2)s, multiplicity=%(mul)s, intrinsic_line_width=0, DebyeWaller_factor=0)," % locals()
        lines_for_peaks.append(line)
        continue

    lines_for_peaks = [l for (q, l) in sorted(zip(qs, lines_for_peaks))]

    lines_for_peaks = '\n'.join('    '+l for l in lines_for_peaks)

    unitcell_volume = lattice.volume
    abs_xs = xsc.abs_xs_at2200

    content = '''from mccomponents.sample.diffraction.SimplePowderDiffractionKernel import Peak
peaks = [
%(lines_for_peaks)s
    ]

# unit: \AA
unitcell_volume = %(unitcell_volume)s

# unit: barns
class cross_sections:
    coh = 0
    inc = 0
    abs = %(abs_xs)s
''' % locals()

    with open('{sample}_peaks.py'.format(sample=samplefile_tosave_scatteringResult), 'wt') as s:
        s.write(content)




