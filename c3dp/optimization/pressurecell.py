import os,sys, numpy as np
from matplotlib import pyplot as plt
from scipy.optimize import differential_evolution
from mcvine import run_script
from c3dp.instrument import DEFAULT_INSTRUMENT_CONFIGURATION

parent_dir = os.path.abspath(os.pardir)
DEFAULT_BEAM_PATH=os.path.join(parent_dir, 'beam')  # directory for possible mcvine neutron sources
mantid_path=os.path.join(parent_dir, 'mantid')
result_path=os.path.join(parent_dir, 'results')

libpath = os.path.join(parent_dir, 'c3dp')

if not libpath in sys.path:
    sys.path.insert(0, libpath)

from c3dp.instrument.collimator.collimator_support import Parameter_error
from exports import convert2nxs as det2nxs
from reduction import reduce_nexasdata_using_mantid as red, rotate_detector_for_reduction_mantid as rot, \
    masking_nexus_givenKernel as mask
from instrument.monitor import conf
from c3dp.optimization.peak import *


class PressureCellBase(object):

    def parameters(self, Snap_angle = False, coll_sim = False,
                   source_file = 'clampcellSi_scattered-neutrons_1e9_det-50_105_new',
                   beam_path=DEFAULT_BEAM_PATH,
                   sampleassembly_fileName = 'collimator_plastic',ncount=1e3, sourceTosample_x = 0.0,
                   sourceTosample_y = 0.0, sourceTosample_z = 0.0,
                   masking = False, masked_template = 'coll_plastic_SCAT_masked.nxs',
                   peaks={'sample':[Si_111_peak,Si_220_peak ], 'cell' : [Al_111_peak,Cu_111_peak,Cu_200_peak]} ):

        self.Snap_angle = Snap_angle
        self.coll_sim = coll_sim
        self.source_file = source_file
        self.beam_path = beam_path
        self.sampleassembly_fileName = sampleassembly_fileName
        self.ncount=ncount
        self.sourceTosample_x = sourceTosample_x
        self.sourceTosample_y = sourceTosample_y
        self.sourceTosample_z = sourceTosample_z
        self.masking = masking
        self.masked_template = masked_template
        self.peaks= peaks

    def source_neutrons(self):
        scattered =os.path.join(self.beam_path, self.source_file)
        return(scattered)

    def create_collimator_geometry(self, params):
        return self.sampleassembly_fileName

    def diffraction_pattern_calculation(self, params=[20, 20], instr=DEFAULT_INSTRUMENT_CONFIGURATION):
        name = self.create_collimator_geometry(params)

        simdir = os.path.join(
            parent_dir,
            "out/%s" %
            (name))

        # scattered_neutrons ='clampcellSi_scattered-neutrons_1e9_det-50_105_new'


        # scatterer = {(sampleassembly_fileName, 'shapeColl', 'coll_geometry', 'H', 'xyz'),
        #              }
        #
        # sa.makeSAXML(sampleassembly_fileName, scatterer)

        # sample= 'collimator_plastic'
        import shutil
        shutil.rmtree(simdir)
        run_script.run_mpi(instr, simdir,
                           beam=self.source_neutrons(), ncount=self.ncount,
                           nodes=20, angleMon1=-50., angleMon2=105., sample=self.sampleassembly_fileName,
                           sourceTosample_x=self.sourceTosample_x, sourceTosample_y=self.sourceTosample_y,
                           sourceTosample_z=self.sourceTosample_z,
                           detector_size=0.45, overwrite_datafiles=True)

        template=os.path.join( mantid_path, 'template.nxs')

        nexus_file_path = os.path.join( mantid_path, '{}.nxs'.format(name))

        det2nxs.create_nexus(simdir, nexus_file_path, template)

        SNAP_definition_file = os.path.join( mantid_path,  'SNAP_virtual_Definition.xml')


        nexus_file_correctDet_path = os.path.join(mantid_path, '{}_correctDet.nxs'.format(name))


        rot.detector_position_for_reduction(nexus_file_path, conf,
                                            SNAP_definition_file, nexus_file_correctDet_path)

        if self.masking :
            masked_file_path = os.path.join(mantid_path, '{}_masked.nxs'.format(name))

            masked_template_path = os.path.join(mantid_path, '{}'.format(self.masked_template) )

            mask.masking(nexus_file_correctDet_path, masked_template_path, masked_file_path)

        else:
            masked_file_path = nexus_file_correctDet_path

        binning = [0.5, 0.01, 4.]
        d_sim, I_sim, error = red.mantid_reduction(masked_file_path, binning)

        plt.figure()
        plt.errorbar (d_sim, I_sim, error)
        plt.xlabel('d_spacing ()')
        plt.show()

        np.save(os.path.join(result_path, 'I_d_{sample}.npy'.format(sample=name)), [d_sim, I_sim, error])

        return (d_sim, I_sim, error)


    # def peak_detection(self, para):



    def collimator_inefficiency(self, params):
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
        return (1/self.collimator_inefficiency(params))


    def objective_func(self,params):
        try:
            return (self.collimator_inefficiency(params))

        except Parameter_error as e:
            return (1e10)

    def optimize(self, params_bounds = [(2.0, 8.0), (17.0, 50.0)]):
        # objective_func.counter = 0

        result = differential_evolution(self.objective_func, params_bounds,popsize=4,maxiter=10)
        with open(os.path.join(result_path, 'optimized_Collimator_Dimension.dat'), "w") as res:
            res.write(result.x)
        return(result.x)
