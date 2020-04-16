import c3dp.instruments.scatkernel.scattering_kernal_program as skp
import  numpy as np
import os
import pytest

thisdir = os.path.dirname(__file__)
DEFAULT_SAMPLE_PATH = os.path.join (thisdir, '../sample')

@pytest.mark.parametrize( 'diffraction_peak_path, '
                         'path_toSave_scaterinfKernel_file, scaterer_type_name, kernel_type,target',
                         [
                             (os.path.join (DEFAULT_SAMPLE_PATH, 'Si'),DEFAULT_SAMPLE_PATH,
                           'sample','elastic',
'''<?xml version="1.0"?>

<!DOCTYPE scatterer>

<!-- weights: absorption, scattering, transmission -->
<homogeneous_scatterer mcweights="0, 1, 3">

    <SimplePowderDiffractionKernel Dd_over_d="1e-05" DebyeWaller_factor="1" peaks-py-path="/home/fi0/c3dp_JOB/second_repo/c3dp/sample/Si_peaks.py">
  </SimplePowderDiffractionKernel>


</homogeneous_scatterer>'''    )])

def test_makeSKXML(diffraction_peak_path,path_toSave_scaterinfKernel_file,
                   scaterer_type_name,kernel_type, target ):
    """
    unit test for 'makeSKXML' function in 'scattering_kernel_program' module

    Parameters
    ----------
    diffraction_peak_path: string
        peaks location of the scatterer
    path_toSave_scaterinfKernel_file: string
        path where the scattering kernel file would be saved
    scaterer_type_name: string
        name of the scatterer type (sample/ cell)
    kernel_type: string
        if the 'elastic or inelastic' kernel to specify
    target: string
        the output result to be evaluated against

    Returns
    -------

    """
    skp.makeSKXML(kernel_type, path_toSave_scaterinfKernel_file,
                  scaterer_type_name, diffraction_peak_path)
    saved_file= os.path.join(path_toSave_scaterinfKernel_file, scaterer_type_name)
    saved_file_name =saved_file+'-scatterer.xml'
    file1 = open(saved_file_name, "r+")
    calculated = list(file1.read())
    target = list(target)
    np.testing.assert_string_equal(calculated[30] ,target[30]
                                   )
