import os,sys, numpy as np
from scipy.optimize import differential_evolution
from mcvine import run_script
import unittest as unittest
from mcni.neutron_storage.idf_usenumpy import totalintensity, count


thisdir = os.path.abspath(os.path.dirname(__file__))
parentpath = os.path.join(thisdir, '..')
beam_path=os.path.join(thisdir, '../beam')

libpath = os.path.join(thisdir, '../simlib')

if not libpath in sys.path:
    sys.path.insert(0, libpath)

from collimator_geometry import create as create_collimator_geometry, Parameter_error
import reduction, conf

scattered =os.path.join( beam_path, 'clampcellSi_neutron')  # path to scattered neutrons from clamp cell and sample
sample = 'collimator'
ncount = 1e5
nodes = 20
sourceTosample=0
detector_size=0.5

instr = os.path.join(libpath, 'myinstrument.py')

scattered_beam_intensity= totalintensity(scattered)*ncount/count(scattered)

samplepath = os.path.join(thisdir, '../sample')
filename='coll_geometry.xml'
outputfile=os.path.join(samplepath, filename)

def objective_func(params):
    try:
        diffraction_pattern = diffraction_pattern_calculation(params)

        return (collimator_inefficiency(diffraction_pattern))

    except Parameter_error as e:
        return (1e10)


def diffraction_pattern_calculation(params):

    number_channels, channel_length = params
    create_collimator_geometry(140,
                               number_channels=int(number_channels),
                               channel_length=channel_length,
                               detector_angles=[-45, -135], outputfile=outputfile, collimator_Nosupport=True,
                               scad_flag=True)
    simdir=os.path.join(
        parentpath,
        "out/optimization-NC_%s-dist_%s" %(number_channels, channel_length))
    run_script.run_mpi(
        instr,simdir, beam=scattered, ncount=ncount, nodes=nodes, sample=sample,
        sourceTosample=sourceTosample, detector_size=detector_size, overwrite_datafiles=True)

    dcs, I_d, error = reduction.reduce_all(simdir, conf, l1=14.699, l2=0.3, l3=0.5, bins=np.arange(0, 4, 0.01))
    return (dcs, I_d, error)

def collimator_inefficiency(diffraction_pattern):
    dcs, I_d, error = diffraction_pattern
    Si_peak_int = I_d[ (dcs<3.5) & (dcs>3)].sum()

    Cu_peak_int=I_d[np.logical_and(dcs<2.2, dcs>2)].sum()

    collimator_performance=(Cu_peak_int/Si_peak_int)+(1-Si_peak_int/scattered_beam_intensity)

    return (collimator_performance)


def optimize():
    # objective_func.counter = 0
    params_bounds = [(2.0, 8.0), (17.0, 50.0)]
    result = differential_evolution(objective_func, params_bounds,popsize=4,maxiter=10)
    with open("optimized_Collimator_Dimension", "w") as res:
        res.write(result.x)
    return(result.x)


