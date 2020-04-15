from c3dp.optimization.optimization_base import PressureCellBase
from instrument.collimator.collimator_geometry_variable_channel_length_blade_thickness \
    import create as create_collimator_geometry


class PresureCell(PressureCellBase):

    def create_collimator_geometry(self, params):
        if  self.coll_sim:

            max_coll_len, wall_size = params

            create_collimator_geometry(
                max_coll_len=max_coll_len,
                mini_ch_wall_thickness=wall_size,
                Snap_angle=self.Snap_angle,
                detector_angles=[-45])

            name = "length_%s-wall-size_%s" % (max_coll_len, wall_size)

        else:
            name = self.sampleassembly_fileName
        return name






















