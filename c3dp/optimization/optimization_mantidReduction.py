from c3dp.optimization.pressurecell import PressureCellBase
from instrument.collimator.collimator_geometry_zigzag import create as create_collimator_geometry

class PresureCell(PressureCellBase):

    def create_collimator_geometry(self, params):
        if  self.coll_sim:
            max_coll_len, coll_front_end_from_center = params

            create_collimator_geometry(
                coll_front_end_from_center=coll_front_end_from_center,
                max_coll_len=max_coll_len,
                Snap_angle= self.Snap_angle,
                detector_angles=[-45])

            name = "length_%s-dist_%s" % (max_coll_len, coll_front_end_from_center)

        else:
            name = self.sampleassembly_fileName
        return name
