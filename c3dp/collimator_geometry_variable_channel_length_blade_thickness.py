from collimator_zigzagBlade import Collimator_geom, Parameter_error
import os, sys
parent_dir = os.path.abspath(os.pardir)
libpath = os.path.join(parent_dir, 'c3dp_source')
sample_path = os.path.join (parent_dir, 'sample')

coll_geo_file_name= 'coll_geometry'
coll_geo_file = os.path.join(sample_path, coll_geo_file_name)

def create (max_coll_len, mini_ch_wall_thickness, channel_size=3.,coll_front_end_from_center= 54. ,Snap_angle=False, vertical_number_channels=20, horizontal_number_channels=20,
            detector_angles=[-45,-135],multiple_collimator=False, collimator_Nosupport=True, scad_flag=False,
            outputfile=coll_geo_file):

    coll=Collimator_geom()
    coll.set_constraints(SNAP_acceptance_angle=Snap_angle,
                         max_coll_height_detector=65.,
                          max_coll_width_detector=160.,
                          min_channel_wall_thickness=mini_ch_wall_thickness,
                          max_coll_length=max_coll_len, min_channel_size=channel_size,
                          collimator_front_end_from_center=coll_front_end_from_center,
                          vertical_odd_blades=False, horizontal_even_blades=False,
                          left_border_odds=False,
                          collimator_parts=False)

    vertical_number_channels = int(coll.Vertical_number_channels(max_coll_len))

    horizontal_number_channels = int(coll.Horizontal_number_channels(max_coll_len))

    print ('number channels in vertical direction: ', vertical_number_channels)

    print ('number channels in horizontal direction: ', horizontal_number_channels)



    coll.set_parameters(vertical_number_channels=vertical_number_channels, horizontal_number_channels=horizontal_number_channels, channel_length=max_coll_len)



    coll.gen_collimators_xml( detector_angles=detector_angles,multiple_collimator=multiple_collimator,
                              collimator_Nosupport=collimator_Nosupport,
                              scad_flag=scad_flag, coll_file=outputfile)




# gen_col__xml(angular_spacing=2, channel_size=1, outsideCurveLength_fromSOurce=50, insideCurveLength_fromSOurce=0, coll_file=outputfile)
