import os,numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import differential_evolution
from mcvine import run_script
from mantid2mcvine.nxs import template as nxs_template

from instruments.collimator.collimator_support import Parameter_error
from exports import convert2nxs as det2nxs
from reduction import reduce_nexasdata_using_mantid as red, rotate_detector_for_reduction_mantid as rot, \
    masking_nexus_givenKernel as mask
from instruments.monitor import conf
from peak import Peak

PARENT_DIR = os.path.abspath(os.pardir)
DEFAULT_BEAM_PATH=os.path.join(PARENT_DIR, 'beam')  # directory for possible mcvine neutron sources
DEFAULT_NEXUS_PATH=os.path.join(PARENT_DIR, 'nexus') # directory to save the nexus files
DEFAULT_RESULT_PATH=os.path.join(PARENT_DIR, 'results') # directory to save the resulted diffraction 1D curve
DEFAULT_SAMPLE_PATH = os.path.join(PARENT_DIR, 'sample') # directory to save the scattering and geometry files for simulation
DEFAULT_COLLIMATOR_GEOMETRY_FILENAME= 'coll_geometry' # default collimator geometry file name
DEFAULT_COLLIMATOR_GEOMETRY_SAVED_PATH = os.path.join(DEFAULT_SAMPLE_PATH, DEFAULT_COLLIMATOR_GEOMETRY_FILENAME) # default path to save collimator geometry
DEFAULT_INSTRUMENT_PATH = os.path.join(PARENT_DIR, 'instruments/myinstrument_multipleDetectors.py')


#### DEFAULT peaks for components of clamp cell #################
Si_111_peak = Peak(label='Si 111', d_spacing=3.345, d_min=3., d_max=3.5)
Al_111_peak = Peak(label='Al 111', d_spacing=2.3, d_min=2.2, d_max=2.5)
Cu_111_peak = Peak(label='Cu 111', d_spacing=2.08, d_min=2., d_max=2.1)
Si_220_peak = Peak(label='Si 220', d_spacing=1.9, d_min=1.86, d_max=2)
Cu_200_peak = Peak(label='Cu 200', d_spacing=1.8, d_min=1.78, d_max=1.85)

class Base(object):
    """
    class to create essential steps for optimization of collimator and performing optimization
    """

    def parameters( self, Snap_angle = False, coll_sim = False  ,
                   source_file = 'clampcellSi_scattered-neutrons_1e9_det-50_105_new',
                    beam_path=DEFAULT_BEAM_PATH,
                    nexus_path = DEFAULT_NEXUS_PATH,
                    result_path=DEFAULT_RESULT_PATH,
                    template =None,
                    SNAP_definition_file =None,
                    nodes=20,
                    sampleassembly_fileName = 'collimator_plastic',
                    path_tosave_collimator_geometry = DEFAULT_COLLIMATOR_GEOMETRY_SAVED_PATH,
                    collimator_detector_width = 160,
                    collimator_detector_height = 65.,
                    min_channel_wall_thickness = 1,
                    min_channel_size = 3.,
                    multiple_collimator = False,
                    collimator_Nosupport = True,
                    scad_flag = False,
                    ncount=1e3, sourceTosample_x = 0.0,
                    sourceTosample_y = 0.0, sourceTosample_z = 0.0, moderatorTosample_z=-42.254,
                    angleMons = [-50, 105] ,
                    collimator_angles=[-45],
                    sampleTodetector_z=[0.5, 0.5], detector_width=[0.5,0.5], detector_height=[0.5, 0.5],
                    number_pixels_in_height=[256, 256],
                    number_pixels_in_width=[256, 256], number_of_box_in_height=[3,3],
                    number_of_box_in_width=[3,3], masking = False,
                    masked_template = 'coll_plastic_SCAT_masked.nxs',
                    binning=[0.5, 0.01, 4.],number_of_detectors= 1,
                    peaks={'sample':[Si_111_peak,Si_220_peak ], 'cell' : [Al_111_peak,Cu_111_peak,Cu_200_peak]}):

        """
        Defining the parameters to run the simulation and to create the geometry of the collimator
        Parameters
        ----------
        Snap_angle : Boolean
            if the conventional SNAP detector angle is used
        coll_sim: Boolean
            if simulating the collimator
        source_file: string
            the incoming beam file to the sample
        beam_path: string
            path to get the incoming beam file to the sample
        nexus_path: string
            path to save nexus files
        result_path: string
            path to save the diffraction results
        template: string
            path to the nexus template of instrument definition file
        SNAP_definition_file: string
            path to the instrument definition file
        nodes: int
            number of nodes to run the simulation
        sampleassembly_fileName: string
            name of the file to save the materials scattering information
        ncount: int
            number of neutrons used for simulation
        sourceTosample_x: float
            source to sample distance along X in m
        sourceTosample_y: float
            source to sample distance along Y in m
        sourceTosample_z: float
            source to sample distance along Z in m
        moderatorTosample_z: float
            moderator to sample distance in m
        angleMons: list
            monitors angular position in degree with respect to beam axis (Z axis)
        collimator_angles: list
            collimator angular position in degree with respect to beam axis (Z axis)
        sampleTodetector_z: list
            sample detector distances in  m
        detector_width: list
            width of the detectors in m
        detector_height: list
            height of the detectors in m
        number_pixels_in_height: int
            number of pixels per bank along height
        number_pixels_in_width: int
            number of pixels per bank along width
        number_of_box_in_height: int
            number of bank along height
        number_of_box_in_width: int
            number of box along width
        masking: bool
            if masking is added or not
        masked_template: string
            the path of the mask
        binning: list
            list of first value, spacing and last value
        number_of_detectors: int
            number of detectors
        peaks: object
            class of the peaks of peaks label, d-spacing value, d minimum and d maximum

        Returns
        -------

        """
        self.beam_path = beam_path
        self.nexus_path = nexus_path
        self.result_path = result_path
        self.Snap_angle = Snap_angle
        self.coll_sim = coll_sim
        self.source_file = source_file
        self.template = template
        self.SNAP_definition_file = SNAP_definition_file
        self.sampleassembly_fileName = sampleassembly_fileName
        self.ncount = ncount
        self.sourceTosample_x = sourceTosample_x
        self.sourceTosample_y = sourceTosample_y
        self.sourceTosample_z = sourceTosample_z
        self.angleMons = angleMons
        self.detector_width = detector_width
        self.detector_height = detector_height
        self.sampleTodetector_z = sampleTodetector_z
        self.number_pixels_in_height = number_pixels_in_height
        self.number_of_box_in_height = number_of_box_in_height
        self.number_pixels_in_width = number_pixels_in_width
        self.number_of_box_in_width = number_of_box_in_width
        self.masking = masking
        self.masked_template = masked_template
        self.peaks = peaks
        self.moderatorTosample_z = moderatorTosample_z
        self.number_of_detectors = number_of_detectors
        self.number_of_total_DetectorPixels = 0
        self.binning= binning
        self.collimator_angles = collimator_angles
        self.nodes = nodes
        self.path_tosave_collimator_geometry = path_tosave_collimator_geometry
        self.collimator_detector_width = collimator_detector_width
        self.collimator_detector_height = collimator_detector_height
        self.min_channel_wall_thickness = min_channel_wall_thickness
        self.min_channel_size = min_channel_size
        self.multiple_collimator = multiple_collimator
        self.collimator_Nosupport = collimator_Nosupport
        self.scad_flag = scad_flag

        for i in range(self.number_of_detectors):
            self.number_of_total_DetectorPixels += self.number_pixels_in_height[i]\
                                              *self.number_of_box_in_height[i]\
                                              *self.number_pixels_in_width[i]\
                                              *self.number_of_box_in_width[i]
    def safe_path_join(self, *args):
        """
        join the path and check if the path exist, if path does not exist, raising the error
        Parameters
        ----------
        args: strings
            any path to be joined

        Returns
        -------
            path : string
                path of any file

        """
        path =os.path.join(*args)
        if os.path.exists(os.path.dirname(path)) is False:
            raise IOError('{} does not exist'.format (path) )
        return path



    def source_neutrons(self):
        """
        creating the path to the source neutrons to be fed to sample assembly
        Returns
        -------
            scattered neutrons: string
                the path of the scattered neutron to be fed to sample assembly
        """
        scattered = self.safe_path_join( self.beam_path, self.source_file )
        return(scattered)

    def create_collimator_geometry(self, params):
        """
        creating collimator geometry to be optimized
        Parameters
        ----------
        params: class parameters

        Returns
        -------

        """
        return self.sampleassembly_fileName

    def diffraction_pattern_calculation(self, params=[20, 20], instr=DEFAULT_INSTRUMENT_PATH, simdir=None):
        """

        Parameters
        ----------
        params
        instr
        simdir

        Returns
        -------

        """
        name = self.create_collimator_geometry(params)

        if simdir is None:
            simdir = os.path.join(
                PARENT_DIR,
                "out/%s" %
                (name))


        run_script.run1_mpi(instr, simdir,
        beam = self.source_neutrons(), ncount = self.ncount,
        nodes = self.nodes,
        angleMons=self. angleMons,
        sample = self.sampleassembly_fileName,
        sourceTosample_x = self.sourceTosample_x,
        sourceTosample_y = self.sourceTosample_y,
        sourceTosample_z = self.sourceTosample_z,
        sampleTodetector_z = self.sampleTodetector_z,
        number_detectors = self.number_of_detectors,
        detector_width = self.detector_width,
        detector_height = self.detector_height,
        number_pixels_in_height = self.number_pixels_in_height,
        number_of_box_in_height = self.number_of_box_in_height,
        number_pixels_in_width = self.number_pixels_in_width,
        number_of_box_in_width = self.number_of_box_in_width,
        overwrite_datafiles = True)


        if self.SNAP_definition_file is None:
            self.SNAP_definition_file = os.path.join(self.nexus_path, 'SNAP_virtual_Definition.xml')

        if self.template is None:
            self.template=os.path.join(self.nexus_path, 'template.nxs')
            nxs_template.create(
                self.SNAP_definition_file,
                ntotpixels=self.number_of_total_DetectorPixels, outpath=self.template, pulse_time_end=1e5
            )

        nexus_file_path = os.path.join(self.nexus_path, '{}.nxs'.format(name))

        det2nxs.create_nexus(simdir, nexus_file_path, self.template, numberOfPixels=self.number_of_total_DetectorPixels)


        nexus_file_correctDet_path = os.path.join(self.nexus_path, '{}_correctDet.nxs'.format(name))


        rot.detector_position_for_reduction(nexus_file_path, conf,
                                            self.SNAP_definition_file, nexus_file_correctDet_path)

        if self.masking :
            masked_file_path = os.path.join(self.nexus_path, '{}_masked.nxs'.format(name))

            mask.masking(nexus_file_correctDet_path, self.masked_template, masked_file_path)

        else:
            masked_file_path = nexus_file_correctDet_path

        binning = self.binning
        d_sim, I_sim, error = red.mantid_reduction(masked_file_path, binning)

        plt.figure()
        plt.errorbar (d_sim, I_sim, error)
        plt.xlabel('d_spacing ()')
        plt.show()

        np.save(os.path.join(self.result_path, 'I_d_{sample}.npy'.format(sample=name)), [d_sim, I_sim, error])

        return (d_sim, I_sim, error)


    def collimator_inefficiency(self, params):
        """

        Parameters
        ----------
        params

        Returns
        -------

        """
        dcs, I_d, error = self.diffraction_pattern_calculation (params)
        sample_peaks = self.peaks['sample']
        cell_peaks = self.peaks['cell']
        sample_peak_int=0.0
        cell_peak_int =0.0
        for sample_peak in sample_peaks:
            sample_peak_int += I_d[ (dcs<sample_peak.dmax) & (dcs>sample_peak.dmin)].sum() #I_d[ (dcs<3.5) & (dcs>3)].sum()
        for cell_peak in cell_peaks:
            cell_peak_int +=  I_d[ (dcs<cell_peak.dmax) & (dcs>cell_peak.dmin)].sum()  #I_d[np.logical_and(dcs<2.2, dcs>2)].sum()
        collimator_ineff = (cell_peak_int / sample_peak_int)  # new objective function suggested by Garrett
        print ('coll_len,:', params[0] , 'focal_distance,:', params[1]  ,'collimator_performance: ', (sample_peak_int/cell_peak_int))
        return (collimator_ineff)

    def collimator_performance (self, params):
        """

        Parameters
        ----------
        params

        Returns
        -------

        """
        return (1/self.collimator_inefficiency(params))


    def objective_func(self,params):
        """

        Parameters
        ----------
        params

        Returns
        -------

        """
        try:
            return (self.collimator_inefficiency(params))

        except Parameter_error as e:
            return (1e10)

    def optimize(self, params_bounds = [(2.0, 8.0), (17.0, 50.0)], population_size=4, maximum_iteration =5):
        """

        Parameters
        ----------
        params_bounds
        population_size
        maximum_iteration

        Returns
        -------

        """
        # objective_func.counter = 0

        result = differential_evolution(self.objective_func, params_bounds,popsize=population_size,maxiter=maximum_iteration)
        with open(os.path.join(self.result_path, 'optimized_Collimator_Dimension.dat'), "w") as res:
            res.write(result.x)
        return(result.x)
