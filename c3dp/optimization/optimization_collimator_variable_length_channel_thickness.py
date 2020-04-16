from optimization_base import Base
from instruments.collimator.collimator_geometry_zigzag import create as create_collimator_geometry

class InstrumentComponent(Base):
    """
    changing the collimator geometry to get optimize geometry of collimator
    """

    def create_collimator_geometry(self, params):
        """
        creating the collimator geometry with variable length and variable channel size
        Parameters
        ----------
        params: list of two floats
            parameters for collimator length and variable channel size

        Returns
        -------
            name : string
                the name of the simulated result file
        """
        if  self.coll_sim:
            max_coll_len, min_channel_size = params

            create_collimator_geometry(
                coll_front_end_from_center=self.coll_front_end_from_center,
                max_coll_len=max_coll_len,
                detector_width = self.collimator_detector_width,
                detector_height = self.collimator_detector_height,
                min_channel_wall_thickness = self.min_channel_wall_thickness,
                min_channel_size = min_channel_size,
                Snap_angle= self.Snap_angle,
                detector_angles= self.collimator_angles,
                multiple_collimator = self.multiple_collimator,
                collimator_Nosupport = self.collimator_Nosupport,
                scad_flag = self.scad_flag,
                outputfile= self.path_tosave_collimator_geometry)

            name = "length_%s-dist_%s" % (max_coll_len, min_channel_size)

        else:
            name = self.sampleassembly_fileName
        return name

