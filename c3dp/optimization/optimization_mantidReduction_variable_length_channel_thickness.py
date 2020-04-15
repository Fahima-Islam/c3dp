from c3dp.optimization.optimization_base import PressureCellBase
from instrument.collimator.collimator_geometry_variable_channel_length_channel_thickness \
    import create as create_collimator_geometry

class PresureCell(PressureCellBase):

    def create_collimator_geometry(self, params):
        if  self.coll_sim:

            max_coll_len, chann_size = params

            create_collimator_geometry(
                channel_size=chann_size,
                max_coll_len=max_coll_len,
                Snap_angle= self.Snap_angle,
                detector_angles=[-45])

            name = "length_%s-dist_%s" % (max_coll_len, chann_size)

        else:
            name = self.sampleassembly_fileName
        return name






