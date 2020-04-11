import os, glob
thisdir = os.path.abspath(os.path.dirname(__file__))
import numpy as np
from mantid2mcvine.nxs import  Events2Nxs

def create_nexus(datadir,fileTOsave, template, numberOfPixels=256,
                 detectorPanel=3, tofBinSize=0.1 ):

    """converting Numpy (.npy) file to Events Nexus (.nxs) file


         Parameters
         ----------
         datadir: string
              name of the output directory of the simulation
         fileTOsave: string
                name of the directory where the Nexus file will be saved
         template: string
                name of the  directory of the template.nxs file
         numberOfPixels: int
                number of the pixela in one detector panel
         detectorPanel: int
                number of the detector panel
         tofBinSize: float
                the bin size for time of flight axis

         Returns
         -------
         Event file in Nexus format
         """

    det = "{directoryName}/*/detector*.npy".format(directoryName=datadir)

    detector = glob.glob(det)


    events=[]

    for npyf in detector:
        narr = np.load(npyf)
        events.append(narr)

    events = np.hstack(events)

    N = numberOfPixels*detectorPanel
    e2n = Events2Nxs.Event2Nxs(template, npixels=2*N*N, nmonitors=0)

    e2n.write(events, tofbinsize=tofBinSize, nxsfile=fileTOsave)


