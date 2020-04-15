import os
template = """<?xml version="1.0"?>

<!DOCTYPE scatterer>

<!-- weights: absorption, scattering, transmission -->
<homogeneous_scatterer mcweights="{absorption}, {scattering}, {transmission}">

  <SimplePowderDiffractionKernel Dd_over_d="{Dd_over_d}" DebyeWaller_factor="{DebyeWaller_factor}" peaks-py-path="{scatterer}_peaks.py">
  </SimplePowderDiffractionKernel>

</homogeneous_scatterer>

"""

def makeSKXML(scatterer,path_ToSave_ScatteringKernel, scatterer_type_name, absorption=0,scattering=1,transmission=3,
              Dd_over_d=1e-5, DebyeWaller_factor=1 ):
   """  making scattering kernel xml file
                      Parameters
                      ----------
                      scatterer: string
                         peaks location of the scatterer
                      path_ToSave_ScatteringKernel : string
                            path where the scattering kernel file would be saved
                      scatterer_type_name: string
                          name of the scatterer type (sample/ cell)
                      absorption: int
                            weight for absorption
                      transmission: int
                            weight for transmission
                      Dd_over_d: float
                            d spacing resolution in Angstrom
                      DebyeWaller_factor: int
                            Debye Waller factor
                      """

   text = template.format(absorption=absorption, scattering=scattering,transmission=transmission,Dd_over_d=Dd_over_d,
                          DebyeWaller_factor=DebyeWaller_factor, scatterer=scatterer)
   with open( os.path.join('{}','{}-scatterer.xml').format(path_ToSave_ScatteringKernel, scatterer_type_name), "w") as sam_new:
       sam_new.write(text)







