import numpy as np
import math
from instrument.geometry.pml import weave
from instrument.geometry import shapes, operations
import os, sys


class DAC(object):

    def __init__(self):

        self.culet_angle = 82.  # degree
        self.table_angle = 82.  # degree
        self.table_length = 2.5  # mm
        self.culet_length = 2.  # mm
        self.girdle_height = 1.11  # mm
        self.girdle_length = 6.  # mm

        self.gasket_diameter = 6.0  # mm
        self.sample_radius = 0.5  # mm
        self.sample_height = 0.4 #0.2 (real height) #1.5  # mm 0.2 mm

        self.seat_bottom_diameter =18.63  #17.88  # mm
        # 18.63 is the "chamfer top length" of the piston that is calculated below (in piston section),
        # seat_bottom_diameter is made same as "chamfer top length" so that seat and piston
        # are exactly glued together
        self.seat_hollow_large_cone_diameter = 5.89  # mm #seat_hollow_top_diamter
        self.seat_top_diameter = 8.001  # mm
        self.seat_hollow_tappered_height = 1.9558  # mm
        self.seat_skirt_height = 5.18  # mm
        self.seat_shaft_height = 6.37  # mm

        self.vision_seat_bottom_diameter = 16.51  # 17.88  # mm
        self.vision_seat_top_diameter = 6.83 #mm
        self.vision_seat_hollow_top_diamter = 6.19 #mm
        self.vision_seat_hollow_bottom_diameter = 2.43 #mm
        self.vision_seat_skirt_height = 8.38 #mm
        self.vision_seat_skirt_angle = 60 #degree
        self.vision_seat_shaft_height = 2.006 #mm
        self.vision_seat_shaft_diameter = 5.89 #mm


        self.piston_chamfer_height = 3.175  # mm
        self.piston_chamfer_angle = 45  # degree
        self.piston_chamfer_base = 24.99  # mm
        self.piston_shaft_height = 23.6728  # mm

        self.body_base = 56.007  # mm
        self.hollow_base = 9.58 + 24.9936  # mm
        self.bar_height = 12.94  # mm

        self.bar_thickness = (self.body_base - self.hollow_base) / 2.




    def angle2span(self, Verticle_distance, angle):
        return (2 * Verticle_distance * np.tan(np.deg2rad(angle / 2)))

    def span2angle(self, distance, distance_fr_sample, ):
        return (2 * (np.rad2deg(np.arctan(distance / (2 * distance_fr_sample)))))

    def size_at_sample_side(self, outsideCurve_length, outsideCurve_radius, insideCurve_radius):
        return ((outsideCurve_length * insideCurve_radius) / outsideCurve_radius)


    def crown_top_triangle_height(self):
        return ((self.table_length/2)/np.tan(np.deg2rad(self.table_angle/2)))


    def pavilion_bottom_triangle_height(self):
        return ((self.culet_length/2)/np.tan(np.deg2rad(self.culet_angle/2)))

    def pavilion_total_triangle_height (self, girdle_length=6.):

        return ((self.pavilion_bottom_triangle_height()/self.culet_length)*girdle_length)

    def pavilion_height (self):
        return(self.pavilion_total_triangle_height()-self.pavilion_bottom_triangle_height())

    def gasket_height (self):

        return ((self.pavilion_height()+self.sample_height/2.)*2)

    def crown_total_triangle_height(self,girdle_length=6.):
        return ((self.crown_top_triangle_height() / self.table_length) * girdle_length)


    def upper_orLower_anvil_height_from_center(self):
        return (self.pavilion_total_triangle_height()+self.girdle_height\
                                                    +self.crown_total_triangle_height()\
                                                    -self.crown_top_triangle_height())

    ###### ANVIL (DIAMOND (C- diffraction)) #############
    def anvil(self, girdle_length=6.):


        crown_top_triangle_height=self.crown_top_triangle_height()

        crown_total_triangle_height = self.crown_total_triangle_height(girdle_length)

        pavilion_bottom_triangle_height=self.pavilion_bottom_triangle_height()

        print ('pavilion from center', pavilion_bottom_triangle_height)

        pavilion_total_triangle_height= self.pavilion_total_triangle_height(girdle_length)

        upper_orLower_anvil_height_from_center= self.upper_orLower_anvil_height_from_center()



        crown_top_cone=operations.translate(shapes.cone(radius='%s *mm' %500, height= '%s*mm' %(crown_top_triangle_height)),
                                            vertical='%s *mm' % (-crown_top_triangle_height))

        crown_total_cone=operations.translate(shapes.cone(radius='%s*mm' % (girdle_length/2,), height= '%s*mm' %crown_total_triangle_height),
                                            vertical='%s *mm' % (-crown_total_triangle_height))

        crown=operations.subtract(crown_total_cone,crown_top_cone)

        pavilion_bottom_cone = operations.translate(shapes.cone(radius='%s *mm' %500., height='%s*mm' %(pavilion_bottom_triangle_height)),
                                              vertical='%s *mm' % (-pavilion_bottom_triangle_height))

        pavilion_total_cone = operations.translate(
            shapes.cone(radius='%s*mm' %(girdle_length / 2), height='%s*mm' %pavilion_total_triangle_height),
            vertical='%s *mm' % (-pavilion_total_triangle_height))

        pavilion=operations.rotate(operations.subtract(pavilion_total_cone,pavilion_bottom_cone),
                                   transversal=1, angle='%s *degree' % (180))

        girdle=shapes.cylinder(radius='%s*mm' %(girdle_length/2.), height='%s*mm' %(self.girdle_height))
        girdle_inplace=operations.translate(girdle, vertical='%s *mm' % (pavilion_total_triangle_height+self.girdle_height/2.))
        crown_inplace= operations.translate(crown, vertical='%s *mm' % (pavilion_total_triangle_height+self.girdle_height+crown_total_triangle_height))

        upper_diamond_anvil=operations.unite(operations.unite(crown_inplace, girdle_inplace), pavilion)

        lower_diamond_anvil = operations.rotate(operations.rotate(upper_diamond_anvil,
                                                                  transversal=1, angle='%s *degree' % (-180)),
                                                vertical=1, angle='%s *degree' % 180)

        # return (operations.unite(upper_diamond_anvil, lower_diamond_anvil))
        #### the following is for changing the gap between two anvil ##########

        upper_diamond_anvil_at_center= operations.translate(upper_diamond_anvil,vertical='%s *mm' % (-pavilion_bottom_triangle_height) )

        upper_diamond_anvil_at_positive_pt_one_from_center = operations.translate(upper_diamond_anvil_at_center,vertical='%s *mm' % (self.sample_height/2.) )

        lower_diamond_anvil_at_neg_pt_one_from_center = operations.rotate(operations.rotate(upper_diamond_anvil_at_positive_pt_one_from_center,
                                                                  transversal=1, angle='%s *degree' % (-180)),
                                                vertical=1, angle='%s *degree' % 180)


        return( operations.unite(upper_diamond_anvil_at_positive_pt_one_from_center,lower_diamond_anvil_at_neg_pt_one_from_center   ))


    ######## GASKET (STEEL)##########
    ## Al is the flange connected with the flange of the anvil
    # def gasket(self):
    #
    #
    #     solid_gasket=operations.rotate(shapes.cylinder(radius=self.sample_radius, height=self.gasket_diameter),
    #                             transversal = 1, angle = '%s *degree' % (90))
    #
    #     self.hollow_inGasket=operations.rotate(shapes.cylinder(radius=self.sample_radius+500., height=self.sample_height),
    #                             transversal = 1, angle = '%s *degree' % (90))
    #
    #     gasket=operations.subtract(solid_gasket, self.hollow_inGasket)
    #
    #     return(gasket)
    #
    # ######## GASKET HOLDER (Al) ##########
    # def gasket_holder(self):
    #     gasket_holder_width = self.gasket_diameter
    #     gasket_holder_thickness= self.sample_radius
    #     gasket_holder_height=self.pavilion_total_triangle_height*2
    #
    #     gasket_holder_case=shapes.block(height='%s *mm' % gasket_holder_height,
    #                           width='%s *mm' % gasket_holder_thickness,
    #                           thickness='%s *mm' % (gasket_holder_width))
    #
    #
    #
    #     gasket_holder=operations.subtract(operations.subtract(gasket_holder_case, self.hollow_inGasket),
    #                                       self.anvil())
    #     return(gasket_holder)



    ######## GSAKET SOURRENDED THE WHOLE SAMPLE+ANVIL (Al+STEEL) ##########
    def sorrounding_gasket(self):
        # gasket_height = self.pavilion_total_triangle_height() * 2


        gasket_solid_case = shapes.cylinder(radius='%s *mm' % (self.gasket_diameter/2.), height= '%s *mm' % (self.gasket_height()))

        hollow_inGasket = shapes.cylinder(radius='%s *mm' % (self.sample_radius), height='%s *mm' % (self.sample_height+500.))

        gasket_hollow_place_for_sample=operations.subtract(operations.subtract(gasket_solid_case, self.anvil(girdle_length=100.)),
                                                           hollow_inGasket)

        return (gasket_hollow_place_for_sample)



    ######## GSAKET SOURRENDED ONLY SAMPLE (Fe, Cr, Ni, Mn) ##########
    def gasket_contact_with_sample(self ):
        sample_height = self.sample_height*0.5

        hollow_inGasket = shapes.cylinder(radius='%s *mm' % (self.sample_radius), height='%s *mm' % (sample_height+500.))

        solid_Gasket_Onlycontact_with_sample = shapes.cylinder(radius='%s *mm' % (self.gasket_diameter / 2.), height='%s *mm' % (sample_height))


        hollow_Gasket_Onlycontact_with_sample = operations.subtract(solid_Gasket_Onlycontact_with_sample, hollow_inGasket )

        return (hollow_Gasket_Onlycontact_with_sample)



    ######## GSAKET SOURRENDED ONLY ANVIL (Al) ##########

    def gasket_contact_with_anvil(self):

        whole_gasket = self.sorrounding_gasket()
        gasket_at_sample_to_subtract  = shapes.cylinder(radius='%s*mm' %(500), height= '%s *mm' % (self.sample_height))

        return (operations.subtract(whole_gasket, gasket_at_sample_to_subtract))


    ######## SEAT (STEEL, Ni, Co, Mo) ##########
    def snap_seat(self):


        seat_hollow_angle= self.table_angle


        seat_smaller_cone_height = (self.seat_skirt_height * self.seat_top_diameter) / \
                                   (self.seat_bottom_diameter - self.seat_top_diameter)

        seat_larger_cone_height = seat_smaller_cone_height + self.seat_skirt_height

        seat_hollow_large_cone_height=(self.seat_hollow_large_cone_diameter/2)/\
                                      np.tan(np.deg2rad(seat_hollow_angle/2))


        seat_hollow_small_cone_height=np.abs(seat_hollow_large_cone_height-self.seat_hollow_tappered_height)

        seat_hollow_small_cone_diameter = (self.seat_hollow_large_cone_diameter / seat_hollow_large_cone_height)\
                                         * seat_hollow_small_cone_height #seat_hollow_bottom_diameter

        #cone has to be translated to center and after translation, the cone is in the negative Y direction
        seat_cone_to_subtract=operations.translate(shapes.cone(radius='%s *mm' % (self.seat_top_diameter/2.+500.),
                                          height='%s *mm' % (seat_smaller_cone_height)),
                                        vertical = '%s *mm' % (-seat_smaller_cone_height))


        seat_larger_cone=operations.translate(shapes.cone(radius='%s *mm' % (self.seat_bottom_diameter/2.),
                                          height='%s *mm' % (seat_larger_cone_height)),
                                          vertical = '%s *mm' % (-seat_larger_cone_height))

        solid_seat_not_atCenter=operations.subtract(seat_larger_cone, seat_cone_to_subtract)

        solid_seat_at_center =operations.translate(solid_seat_not_atCenter,
                                         vertical = '%s *mm' % (seat_smaller_cone_height)) #solid seat at center(0,0)


        ######## HOLLOW TAPPERED CONE #########
        seat_hollow_large_cone=operations.translate(shapes.cone(radius='%s *mm' % (self.seat_hollow_large_cone_diameter/2.),
                                          height='%s *mm' % (seat_hollow_large_cone_height)),
                                        vertical = '%s *mm' % (-(seat_hollow_large_cone_height)))
        seat_hollow_small_cone_height_sudo=1.
        seat_hollow_small_cone = operations.translate(shapes.cone(radius='%s *mm' % (seat_hollow_small_cone_diameter/2.+50.),
                                                                  height='%s *mm' % (seat_hollow_small_cone_height_sudo)),
                                                      vertical='%s *mm' % (-seat_hollow_small_cone_height_sudo))

        seat_tappered_hollow_not_center= operations.subtract(seat_hollow_large_cone, seat_hollow_small_cone)



        seat_tappered_hollow_at_center= operations.translate(seat_tappered_hollow_not_center,
                                        vertical = '%s *mm' % (seat_hollow_small_cone_height_sudo))

        # invert the tappered hollow
        seat_tappered_hollow=operations.translate(operations.rotate(seat_tappered_hollow_at_center,
                                transversal=1, angle='%s *degree' %(-180)),
                                vertical='%s *mm' % (-self.seat_hollow_tappered_height))

        hollow_seat= operations.subtract(solid_seat_at_center, seat_tappered_hollow)



        smaller_saft_to_drill= shapes.cylinder(radius='%s *mm' % (seat_hollow_small_cone_diameter/2.),
                                               height='%s *mm' % (self.seat_shaft_height+100.))

        seat_withSmall_hollow_shaft=operations.subtract(hollow_seat, smaller_saft_to_drill)

        ######## CYLINDER SHAFT #############
        solid_shaft = shapes.cylinder(radius='%s *mm' % (self.seat_top_diameter / 2.), height='%s *mm' % (self.seat_shaft_height))
        shaft_to_drill = shapes.cylinder(radius='%s *mm' % (self.seat_hollow_large_cone_diameter / 2.),
                                         height='%s *mm' % (self.seat_shaft_height + 100.))

        hollow_shaft_atCenter= operations.translate(operations.subtract(solid_shaft, shaft_to_drill),
                                           vertical='%s *mm' % (-self.seat_shaft_height/2.))

        hollow_shaft_atSkirt=operations.translate(hollow_shaft_atCenter,
                            vertical='%s *mm' % (-self.seat_skirt_height))

        ######## COMBINING  SEAT AND SHAFT #############
        seat_shaft_down_center=operations.unite(seat_withSmall_hollow_shaft, hollow_shaft_atSkirt)

        return (seat_shaft_down_center)

        ######## SEAT (STEEL, Ni, Co, Mo) ##########
    def vision_seat(self):
        seat_hollow_angle = self.table_angle

        seat_larger_cone_height = (self.vision_seat_bottom_diameter/ 2) / \
                                        np.tan(np.deg2rad(self.vision_seat_skirt_angle / 2))

        # seat_smaller_cone_height = (self.vision_seat_skirt_height * self.seat_top_diameter) / \
        #                            (self.seat_bottom_diameter - self.seat_top_diameter)

        seat_smaller_cone_height = seat_larger_cone_height - self.vision_seat_skirt_height

        seat_hollow_large_cone_height_at_top_seat = ((self.vision_seat_hollow_top_diamter) / 2) / \
                                        np.tan(np.deg2rad(seat_hollow_angle / 2))

        seat_hollow_large_cone_height = seat_hollow_large_cone_height_at_top_seat +50

        seat_hollow_large_cone_diameter = 2*seat_hollow_large_cone_height*np.tan(np.deg2rad(seat_hollow_angle/2))



        # cone has to be translated to center and after translation, the cone is in the negative Y direction
        seat_cone_to_subtract = operations.translate(
            shapes.cone(radius='%s *mm' % (self.seat_top_diameter / 2. + 500.),
                        height='%s *mm' % (seat_smaller_cone_height)),
            vertical='%s *mm' % (-seat_smaller_cone_height))

        seat_larger_cone = operations.translate(shapes.cone(radius='%s *mm' % (self.vision_seat_bottom_diameter / 2.),
                                                            height='%s *mm' % (seat_larger_cone_height)),
                                                vertical='%s *mm' % (-seat_larger_cone_height))

        solid_seat_not_atCenter = operations.subtract(seat_larger_cone, seat_cone_to_subtract)

        solid_seat_at_center = operations.translate(solid_seat_not_atCenter,
                                                    vertical='%s *mm' % (
                                                        seat_smaller_cone_height))  # solid seat at center(0,0)

        ######## HOLLOW TAPPERED CONE #########
        seat_hollow_large_cone = operations.translate(
            shapes.cone(radius='%s *mm' % ((seat_hollow_large_cone_diameter) / 2.),
                        height='%s *mm' % (seat_hollow_large_cone_height)),
            vertical='%s *mm' % (-(seat_hollow_large_cone_height)))


        # invert the tappered hollow


        seat_tappered_hollow = operations.translate(operations.rotate(seat_hollow_large_cone,
                                                                      transversal=1, angle='%s *degree' % (-180)),
                                                    vertical='%s *mm' % (-seat_hollow_large_cone_height_at_top_seat))



        hollow_seat = operations.subtract(solid_seat_at_center, seat_tappered_hollow)



        smaller_saft_to_drill = shapes.cylinder(radius='%s *mm' % (self.vision_seat_hollow_bottom_diameter / 2.),
                                                height='%s *mm' % (self.vision_seat_shaft_height + 100.))



        seat_withSmall_hollow_shaft = operations.subtract(hollow_seat, smaller_saft_to_drill)

        ######## CYLINDER SHAFT #############
        solid_shaft = shapes.cylinder(radius='%s *mm' % (self.vision_seat_shaft_diameter / 2.),
                                      height='%s *mm' % (self.vision_seat_shaft_height))

        shaft_to_drill = shapes.cylinder(radius='%s *mm' % (self.vision_seat_hollow_bottom_diameter / 2.),
                                         height='%s *mm' % (self.seat_shaft_height + 100.))

        hollow_shaft_atCenter = operations.translate(operations.subtract(solid_shaft, shaft_to_drill),
                                                     vertical='%s *mm' % (-self.vision_seat_shaft_height / 2.))

        hollow_shaft_atSkirt = operations.translate(hollow_shaft_atCenter,
                                                    vertical='%s *mm' % (-self.vision_seat_skirt_height))

        ######## COMBINING  SEAT AND SHAFT #############
        seat_shaft_down_center = operations.unite(seat_withSmall_hollow_shaft, hollow_shaft_atSkirt)

        return (seat_shaft_down_center)

    def snap_piston(self):
        shaft_height = self.piston_shaft_height - self.piston_chamfer_height
        shaft_hollow = self.seat_top_diameter

        chamfer_big_cone_height = (self.piston_chamfer_base / 2.) * np.tan(np.deg2rad(self.piston_chamfer_angle))

        subtraction_coneHeight_chamfer = chamfer_big_cone_height - self.piston_chamfer_height

        print ('chamfer_top_length',
               (self.piston_chamfer_base / chamfer_big_cone_height) * subtraction_coneHeight_chamfer)

        champfer_big_cone = operations.translate(shapes.cone(radius='%s *mm' % (self.piston_chamfer_base / 2.),
                                                             height='%s *mm' % (chamfer_big_cone_height)),
                                                 vertical='%s *mm' % (-(chamfer_big_cone_height)))

        subtraction_cone_chamfer = operations.translate(shapes.cone(radius='%s *mm' % (500.),
                                                                    height='%s *mm' % (subtraction_coneHeight_chamfer)),
                                                        vertical='%s *mm' % (-(subtraction_coneHeight_chamfer)))

        chamfer_atCenter = operations.translate(operations.subtract(champfer_big_cone,
                                                                    subtraction_cone_chamfer),
                                                vertical='%s *mm' % (subtraction_coneHeight_chamfer))
        ##### SHAFT #########
        shaft_solid = shapes.cylinder(radius='%s *mm' % (self.piston_chamfer_base / 2.),
                                      height='%s *mm' % (shaft_height))

        shaft_in_place = operations.translate(shaft_solid, vertical='%s *mm'
                                                                    % (-(
                shaft_height / 2. + self.piston_chamfer_height)))

        #### CHAMFER+SHAFET ####

        chamfer_shaft = operations.unite(chamfer_atCenter, shaft_in_place)
        subtraction_cylinder_shaft = shapes.cylinder(radius='%s *mm' % (shaft_hollow / 2.), height='%s *mm' % (500))

        piston_down_center = operations.subtract(chamfer_shaft, subtraction_cylinder_shaft)
        return (piston_down_center)

    ######## PISTON( VISION PISTON )(CuBe) ##########
    def vision_piston(self):


        shaft_height = self.piston_shaft_height-self.piston_chamfer_height
        shaft_hollow =  self.vision_seat_top_diameter

        chamfer_big_cone_height= (self.piston_chamfer_base/2.)*np.tan(np.deg2rad(self.piston_chamfer_angle))

        subtraction_coneHeight_chamfer=chamfer_big_cone_height-self.piston_chamfer_height

        print ('chamfer_top_length',
               (self.piston_chamfer_base/chamfer_big_cone_height)*subtraction_coneHeight_chamfer )



        champfer_big_cone=operations.translate(shapes.cone(radius='%s *mm' % (self.piston_chamfer_base/2.),
                                          height='%s *mm' % (chamfer_big_cone_height)),
                                        vertical = '%s *mm' % (-(chamfer_big_cone_height)))

        subtraction_cone_chamfer = operations.translate(shapes.cone(radius='%s *mm' % (500.),
                                          height='%s *mm' % (subtraction_coneHeight_chamfer)),
                                        vertical = '%s *mm' % (-(subtraction_coneHeight_chamfer)))

        chamfer_atCenter = operations.translate(operations.subtract(champfer_big_cone,
                                            subtraction_cone_chamfer),
                                            vertical='%s *mm' % (subtraction_coneHeight_chamfer))
        ##### SHAFT #########
        shaft_solid = shapes.cylinder(radius='%s *mm' % (self.piston_chamfer_base/2.), height='%s *mm' % (shaft_height))


        shaft_in_place=operations.translate(shaft_solid,vertical='%s *mm'
                                 % (-(shaft_height/2. +self.piston_chamfer_height)))

        #### CHAMFER+SHAFET ####

        chamfer_shaft= operations.unite(chamfer_atCenter, shaft_in_place)
        subtraction_cylinder_shaft = shapes.cylinder(radius='%s *mm' % (shaft_hollow / 2.), height='%s *mm' % (500))

        piston_down_center= operations.subtract(chamfer_shaft, subtraction_cylinder_shaft)
        return (piston_down_center)


    ####### SEAT+PISTON (STEEL) ###############
    def snap_seat_piston(self):
        seat= self.snap_seat()
        piston=self.snap_piston()

        piston_Not_just_below_seat_= operations.translate(piston,vertical='%s *mm'
                                 % (-(self.seat_skirt_height/2. +self.seat_shaft_height)))

        piston_below_seat = operations.translate(piston, vertical='%s *mm' % (-(self.seat_skirt_height)))

        seat_W_piston = operations.unite(seat, piston_below_seat )

        # seat_W_piston_below_dac= operations.translate(seat_W_piston,vertical='%s *mm'
        #                          % (-(self.pavilion_total_triangle_height() +self.girdle_height)))

        seat_W_piston_below_dac = operations.translate(seat_W_piston, vertical='%s *mm' % (-(
                self.pavilion_height() + self.sample_height/2.+ self.girdle_height)))

        seat_W_piston_above_dac = operations.rotate(operations.rotate(seat_W_piston_below_dac,
                                transversal=1, angle='%s *degree' %(180)),
                                vertical=1, angle='%s *degree' %-180)

        seat_piston_both= operations.unite(seat_W_piston_below_dac, seat_W_piston_above_dac)
        return (seat_piston_both)

    def vision_seat_piston(self):
        seat= self.vision_seat()
        piston=self.vision_piston()

        piston_Not_just_below_seat_= operations.translate(piston,vertical='%s *mm'
                                 % (-(self.vision_seat_skirt_height/2. +self.vision_seat_shaft_height)))

        piston_below_seat = operations.translate(piston, vertical='%s *mm' % (-(self.vision_seat_skirt_height)))

        seat_W_piston = operations.unite(seat, piston_below_seat )

        # seat_W_piston_below_dac= operations.translate(seat_W_piston,vertical='%s *mm'
        #                          % (-(self.pavilion_total_triangle_height() +self.girdle_height)))

        seat_W_piston_below_dac = operations.translate(seat_W_piston, vertical='%s *mm' % (-(
                self.pavilion_height() + self.sample_height/2.+ self.girdle_height)))

        seat_W_piston_above_dac = operations.rotate(operations.rotate(seat_W_piston_below_dac,
                                transversal=1, angle='%s *degree' %(180)),
                                vertical=1, angle='%s *degree' %-180)

        seat_piston_both= operations.unite(seat_W_piston_below_dac, seat_W_piston_above_dac)
        return (seat_piston_both)

    ###### CBODY-BAR (Cu-Be) ############
    def body_bar(self):


        bar = shapes.cylinder(radius='%s *mm' % (self.bar_thickness/2.), height= '%s *mm' % (self.bar_height))

        bar_in_place_right= operations.translate(bar,beam='%s *mm'
                                 % (-(self.piston_chamfer_base/2.+self.bar_thickness/2.)))
        bar_in_place_left = operations.translate(bar, beam='%s *mm'
                                        % ((self.piston_chamfer_base / 2. + self.bar_thickness / 2.)))

        bar_in_place = operations.unite (bar_in_place_right, bar_in_place_left)

        return(bar_in_place)

    def body_bar_rotated(self):
        return (operations.rotate(self.body_bar(),
                                vertical=1, angle='%s *degree' %(90)))



    ####### SAMPLE ######### ( the sample is a cylinder)
    def sample(self):
        sample_radius = self.sample_radius*0.95
        sample_height = self.sample_height*0.50

        sample= shapes.cylinder(radius='%s *mm' % (sample_radius), height='%s *mm' % (sample_height))
        return(sample)





