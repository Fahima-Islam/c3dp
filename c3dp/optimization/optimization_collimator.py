from optimization_base import Optimizer
from instruments.collimator.collimator_geometry_zigzag import create as create_collimator_geometry

class InstrumentComponent(Optimizer):
    """
    changing the collimator geometry to get optimize geometry of collimator
    """

    def create_collimator_geometry(self, params):
        """
        creating the collimator geometry with variable length and variable distance from sample center to front end of the collimator
        Parameters
        ----------
        params: list of two floats
            parameters for collimator length and the distance of collimator front end from the sample center

        Returns
        -------
            name : string
                the name of the simulated result file
        """
        if  self.coll_sim:
            max_coll_len, coll_front_end_from_center = params

            create_collimator_geometry(
                coll_front_end_from_center=coll_front_end_from_center,
                max_coll_len=max_coll_len,
                detector_width = self.collimator_detector_width,
                detector_height = self.collimator_detector_height,
                min_channel_wall_thickness = self.min_channel_wall_thickness,
                min_channel_size = self.min_channel_size,
                Snap_angle= self.Snap_angle,
                detector_angles= self.collimator_angles,
                multiple_collimator = self.multiple_collimator,
                collimator_Nosupport = self.collimator_Nosupport,
                scad_flag = self.scad_flag,
                outputfile= self.path_tosave_collimator_geometry)

            name = "length_%s-dist_%s" % (max_coll_len, coll_front_end_from_center)

        else:
            name = self.sampleassembly_fileName
        return name

