import os, sys,numpy as np
import math
from instrument.geometry.pml import weave
from instrument.geometry import shapes, operations

thisdir = os.path.abspath(os.path.dirname(__file__))
libpath = os.path.join(thisdir, '../simlib')
if not libpath in sys.path:
    sys.path.insert(0, libpath)

# from collimator_fun_ori_constant_thickness_2_support_mod_3 import Collimator_geom
from collimator_fun_ori_constant_thickness_2_moveBlades import Collimator_geom

from clampcell_geo import Clampcell



clampcell=Clampcell(total_height=False)
outer_body=clampcell.outer_body()
inner_sleeve=clampcell.inner_sleeve()
sample=clampcell.sample()

sample_assemblyCad=operations.unite(operations.unite(outer_body, sample), inner_sleeve)

detector_angles=[-45,-135]

###########################################################
#############################################################333
##########################################################3
min_dis=30.

coll = Collimator_geom()
coll.set_constraints()
coll.set_parameters(number_channels=4.,channel_length =min_dis)

changle_horizontal=coll.horizontal_channel_angle

chan_open_horizontal=coll.angle2span(min_dis,changle_horizontal)

# detector_width=coll.angle2span(500, coll.horizontal_angular_coverage)

# detector_height=coll.angle2span(500, coll.vertical_angular_coverage)

print ('test arc length', np.deg2rad(57)*10)

# print ('length', coll.max_dist_fr_sample_center-min_dis)

# print('detector width in mm', detector_width)
# print ('detector height in mm', detector_height)

print ('sample side channel open horizontally in mm', chan_open_horizontal)
print ('horizintal angular opening of channel', changle_horizontal)

changle_vertical=coll.vertical_channel_angle

chan_open_vertical=coll.angle2span(min_dis,changle_vertical)

print ('vertical angular opening of channel', changle_vertical)

print ('sample side channel open vertically in mm', chan_open_vertical)


# print ('calculated angular coverage', coll.vertical_angular_coverage)

print ('min angle', coll.vertical_pillar_angle_list[0])

print ('max angle', coll.vertical_pillar_angle_list[-1])

channels=coll.generate_collimator_channels()
# pyr=coll.generate_collimator_channels_pyramid()

# rot=coll.tab_screw()

# cut_cyllinder=coll.cylinder()
# coll=collimator_geom(angular_range=[-9, 9],number_channels=20, channel_size=3.9,outsideCurveLength_from_SOurceCenter=170.0,insideCurveLength_from_SOurceCenter=18.0)

collimator=coll.gen_collimators(detector_angles=[0])
# channels=coll.generate_collimator_channels()
# outside_sphere, inside_sphere=coll.spheres()
# cut=coll.gen_top_bottom_right_left_sides()

# conesD,conesU=coll.gen_up_down_cones()

# print ('vertical angle list+90', coll.vertical_pyramid_angle_list+90)

# bpttpm=coll.cylinder()

# sample_assemblyCad=operations.subtract(channels, inside_sphere)

# support=coll.support()
# blade_cuitting_box=coll.generate_box_toCut_big_end()
# blade1, support_design=coll.support_design()
# print coll.min_dist_fr_sample_center*2

# sample_assemblyCad=operations.unite(support, support_design)
# sample_assemblyCad=operations.unite(collimator, blade_cuitting_box)
sample_assemblyCad=operations.unite(outer_Al,collimator)
# print ('coll-height-width',coll.height_width_collimatorSurface_nearTOdetector())

# angles = np.linspace(coll.min_angle, coll.max_angle, num=coll.number_channels)
#
#
# ch_size=(np.array([coll.channel_size*np.cos(np.deg2rad(a)) for a in angles])/coll.outsideCurveLength_from_SOurceCenter)*coll.insideCurveLength_from_SOurceCenter
#
# print ('chanel_sizeSample', ch_size)
#
# total_angularCoverage = angles[-1] - angles[0]
# print (angles[-1])
# print (angles[0])
# print (angles)
# print (total_angularCoverage)
# print ((angles[1]-angles[0]))
#
# print (coll.angular_spacing_between_channels, coll.angularOpenning_ofthe_channels(), 'Center to center gap_channels_mm', coll.center_distance_between_channelsNearTodetector_mm())
#
# print('center_distance_at sample', coll.gap_between_channelsNearTosample_mm())
#
#
#
# print ('gap',coll.gap_between_channelsNearTosample_mm()-np.max(ch_size) )
# print ('total width at sample', coll.height_width_collimatorSurface_nearTOsample())
# print (np.tan(np.pi / 2 - (coll.total_angularCoverage * np.pi / 180 / 2.)))
#
# print (np.tan(np.deg2rad(coll.total_angularCoverage/2)))
#
# print(coll.total_angularCoverage * np.pi / 180 / 2. , np.rad2deg(np.pi/2))
#
# print (np.tan(
#             np.pi- (coll.total_angularCoverage * np.pi / 180. / 2.)))

       # with open ('Al_largest_cone.xml','wt') as file_h:
#     weave(Al_largest_cone,file_h, print_docs = False)
# with open ("Al_largest_cone_widertip.xml",'wt') as file_h:
#     weave(Al_largest_cone_widertip,file_h, print_docs = False)
# with open ("Al_tapered_cylinder.xml",'wt') as file_h:
#     weave(Al_tapered_cylinder,file_h, print_docs = False)
# with open("Al_centered_taperedCylinder.xml", 'wt') as file_h:
#     weave(Al_centered_taperedCylinder, file_h, print_docs=False)
# with open ("outer_Al.xml",'wt') as file_h:
#     weave(outer_Al,file_h, print_docs = False)
#
#
#
# with open ("CuBe_largest_cone.xml",'wt') as file_h:
#     weave(CuBe_largest_cone,file_h, print_docs = False)
# with open ("CuBe_largest_cone_widertip.xml",'wt') as file_h:
#     weave(CuBe_largest_cone_widertip,file_h, print_docs = False)
# with open ("CuBe_tapered_cylinder.xml",'wt') as file_h:
#     weave(CuBe_tapered_cylinder,file_h, print_docs = False)
# with open("CuBe_centered_taperedCylinder.xml", 'wt') as file_h:
#     weave(CuBe_centered_taperedCylinder, file_h, print_docs=False)
# with open ("CuBe_innerSleeve.xml",'wt') as file_h:
#     weave(CuBe_innerSleeve,file_h, print_docs = False)
#
# with open ("sample.xml",'wt') as file_h:
#     weave(sample,file_h, print_docs = False)
#collimator_4channels_22mm_fr_smpl



with open ("collimator_support_ed2.xml",'wt') as file_h:
    weave(sample_assemblyCad,file_h, print_docs = False)