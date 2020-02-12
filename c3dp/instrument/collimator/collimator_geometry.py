from c3dp.instrument.collimator.collimator_zigzagBlade_old import Collimator_geom

def create (coll_length, number_channels, channel_length,detector_angles=[-45,-135],multiple_collimator=True, collimator_Nosupport=True, scad_flag=False,
    outputfile='coll_geometry.xml'):
    coll=Collimator_geom()
    coll.set_constraints(max_coll_height_detector=230., max_coll_width_detector=230.,
                         min_channel_wall_thickness=1.,
                         max_coll_length=coll_length, min_channel_size=3.,
                         truss_base_thickness=30., trass_final_height_factor=0.66, touch_to_halfcircle=6,
                         SNAP_acceptance_angle=False)

    coll.set_parameters(number_channels=number_channels, channel_length=channel_length)


    coll.gen_collimators_xml( detector_angles=detector_angles,multiple_collimator=multiple_collimator,
                              collimator_Nosupport=collimator_Nosupport,
                              scad_flag=scad_flag, coll_file=outputfile)




