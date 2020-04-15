import numpy as np
from instrument.geometry import shapes, operations
from render import renderin_the_file

class Clampcell(object):
    """A class to create the  geometry of different components of the clampcell and the sample that the cell can
    hold in it.

    """

    def __init__(self, total_height=False, sample_height=28.57, total_cell_height=95.758, arbitrary_height_increment=10):
        """Initialization

          Initialization the total height of the cell-sample assembly for simulation

          Parameters
          ----------
          total_height: bool
            if the total height is sample height or cell, default is False, that means total height is the sample height
          sample_height: float
            the height of the sample
          total_cell_height: float
             the height of the
          arbitrary_height_increment: float
                used for the increment of the inner dimension to subtract from outer dimension

          """

        self.sample_height=sample_height #mm
        self.arbitrary_height_increment = arbitrary_height_increment

        if total_height is True:
            self.sample_height=total_cell_height


    ###### OUTER BODY #############
    def outer_body(self, outer_dia=32.05, cone_dia=14.59, incone_angle=2.):
        """
             creating the cylindrical outer body geometry of clampcell

             Parameters
             ----------
             outer_dia: float
                outer diamter of the cylinder in mm
             cone_dia: float
                cone diameter in mm
             incone_angle: float
                the angle of the cone in degree

             Returns
             -------
             geometry of the outer body: object
             """
        Al_OutDiameter = outer_dia # mm
        Al_OutRadius=Al_OutDiameter/2
        Al_Height=self.sample_height #28.57 #mm (total height 95.758 mm)
        Al_InSmallestCone_Dia= cone_dia #mm (inner boundary is tappered cylinder, bottom Diameter )
        Al_InSmallestCone_Rad=Al_InSmallestCone_Dia/2
        Al_InconeAngle= incone_angle

        Al_InHeight=Al_Height+self.arbitrary_height_increment #mm (tappered cylinder height) (this should be same as Al_Height,
        # but in constructive geometry the inner height has to be larger for correct subtraction)

        Al_InLargestCone_Dia= (2* np.tan(np.deg2rad(Al_InconeAngle/2))*Al_InHeight)+Al_InSmallestCone_Dia #( tappered cylinder top diameter)
        Al_InLargestCone_Rad=Al_InLargestCone_Dia/2
        Al_InSmallest_ConeHeight=Al_InSmallestCone_Dia/(2*np.tan(np.deg2rad(Al_InconeAngle/2)))
        Al_InLargest_ConeHeight=Al_InSmallest_ConeHeight+Al_InHeight
        Al_boxHeightToSubtract=Al_InSmallest_ConeHeight*2
        Al_boxthisckness= Al_InSmallestCone_Dia+self.arbitrary_height_increment
        Al_HalfHeight=Al_InHeight/2
        Al_moving_height=Al_InSmallest_ConeHeight+Al_HalfHeight

        ### CReate the string for OUTER BODY ######
        Al_OutRadius_str=str(Al_OutRadius)+r'*mm'
        Al_Height_str=str(Al_Height)+r'*mm'
        Al_InLargestCone_Rad_str=str(Al_InLargestCone_Rad)+r'*mm'
        Al_InLargest_ConeHeight_str=str(Al_InLargest_ConeHeight)+r'*mm'
        Al_InSmallest_ConeHeight_str=str(Al_InSmallest_ConeHeight)+r'*mm'
        Al_boxHeightToSubtract_str=str(Al_boxHeightToSubtract)+r'*mm'
        Al_boxthisckness_str=str(Al_boxthisckness)+r'*mm'
        Al_moving_height_str=str(-Al_moving_height)+r'*mm'


        #create the inner Al largest cone
        Al_largest_cone=shapes.cone(radius=Al_InLargestCone_Rad_str, height=Al_InLargest_ConeHeight_str) # upside down
        #rotation to make top wider
        Al_largest_cone_widertip=operations.rotate(Al_largest_cone, angle="180*deg",vertical="0",transversal="1",beam="0")
        #make a tapered cylinder
        Al_tapered_cylinder= operations.Difference(Al_largest_cone_widertip,
                                                shapes.block(thickness=Al_boxthisckness_str,height=Al_boxHeightToSubtract_str,
                                                             width=Al_boxthisckness_str) )
        #moving the center of the cylinder to the center of the coordinate
        Al_centered_taperedCylinder=operations.translate(Al_tapered_cylinder, vertical=Al_moving_height_str)

        #Creating the outer Al body
        outer_Al = operations.subtract(
            shapes.cylinder(radius=Al_OutRadius_str, height=Al_Height_str),
            Al_centered_taperedCylinder,
            )
        return(outer_Al)



    ######## INNER SLEEVE ##########
    def inner_sleeve(self, inner_dia=4.7, outer_bottom_dia=14.63, outer_cone_angle=2 ):
        """
                  creating the hollow cylindrical inner sleeve geometry of clampcell

                  Parameters
                  ----------
                  inner_dia: float
                     inner diamter of the cylinder in mm
                  outer_bottom_dia: float
                     bottom diameter of the outer cylinder in mm
                  outer_cone_angle: float
                     the angle of the tappered cone in degree

                  Returns
                  -------
                  geometry of the inner sleeve: object
                  """
        CuBe_InDiameter = inner_dia # mm
        CuBe_InRadius=CuBe_InDiameter/2
        CuBe_InHeight=self.sample_height+self.arbitrary_height_increment #mm (total height 95.758 mm)
        CuBe_Height=self.sample_height
        CuBe_OutSmallestCone_Dia=outer_bottom_dia #(outer boundary is tappered cylinder, bottom diameter )
        CuBe_OutSmallestCone_Rad=CuBe_OutSmallestCone_Dia/2
        CuBe_OutconeAngle= outer_cone_angle # the tappered angle

        CuBe_OutLargestCone_Dia= (2* np.tan(np.deg2rad(CuBe_OutconeAngle/2))*CuBe_Height)+CuBe_OutSmallestCone_Dia #( tappered cylinder top diamter)
        CuBe_OutLargestCone_Rad=CuBe_OutLargestCone_Dia/2
        CuBe_OutSmallest_ConeHeight=CuBe_OutSmallestCone_Dia/(2*np.tan(np.deg2rad(CuBe_OutconeAngle/2)))
        CuBe_OutLargest_ConeHeight=CuBe_OutSmallest_ConeHeight+CuBe_Height
        CuBe_boxHeightToSubtract=CuBe_OutSmallest_ConeHeight*2
        CuBe_boxthisckness= CuBe_OutSmallestCone_Dia+self.arbitrary_height_increment
        CuBe_HalfHeight=CuBe_Height/2
        CuBe_moving_height=CuBe_OutSmallest_ConeHeight+CuBe_HalfHeight

        ### CReate the string for INNER SLEEVE ######
        CuBe_InRadius_str=str(CuBe_InRadius)+r'*mm'
        CuBe_InHeight_str=str(CuBe_InHeight)+r'*mm'
        CuBe_Height_str=str(CuBe_Height)+r'*mm'
        CuBe_OutLargestCone_Rad_str=str(CuBe_OutLargestCone_Rad)+r'*mm'
        CuBe_OutLargest_ConeHeight_str=str(CuBe_OutLargest_ConeHeight)+r'*mm'
        CuBe_boxHeightToSubtract_str=str(CuBe_boxHeightToSubtract)+r'*mm'
        CuBe_boxthisckness_str=str(CuBe_boxthisckness)+r'*mm'
        CuBe_moving_height_str=str(-CuBe_moving_height)+r'*mm'

        #create the outer CuBe largest cone
        CuBe_largest_cone=shapes.cone(radius=CuBe_OutLargestCone_Rad_str, height=CuBe_OutLargest_ConeHeight_str) # upside down
        #rotation to make top wider
        CuBe_largest_cone_widertip=operations.rotate(CuBe_largest_cone, angle="180*deg",vertical="0",transversal="1",beam="0")
        #make a tapered cylinder
        CuBe_tapered_cylinder= operations.Difference(CuBe_largest_cone_widertip,
                                                shapes.block(thickness=CuBe_boxthisckness_str,height=CuBe_boxHeightToSubtract_str,
                                                             width=CuBe_boxthisckness_str) )
        #moving the center of the cylinder to the center of the coordinate
        CuBe_centered_taperedCylinder=operations.translate(CuBe_tapered_cylinder, vertical=CuBe_moving_height_str)

        #Creating the InnerSleeve
        CuBe_innerSleeve = operations.subtract(
            CuBe_centered_taperedCylinder,
            shapes.cylinder(radius=CuBe_InRadius_str, height=CuBe_InHeight_str),

            )
        return(CuBe_innerSleeve)

    ####### SAMPLE ######### ( the sample is a cylinder)
    def sample(self, sample_dia=4.16):
        """
                   creating the solid cylindrical sample geometry of clampcell

                   Parameters
                   ----------
                   sample_dia: float
                      diameter of the cylindrical sample in mm

                   Returns
                   -------
                   geometry of the sample: object
                   """
        sample_Height=self.sample_height #mm
        sample_Diameter=sample_dia #mm
        sample_Radius=sample_Diameter/2

        ##covert to string###
        sample_Height_str=str(sample_Height)+r'*mm'
        sample_Radius_str=str(sample_Radius)+r'*mm'
        ##cylindrical sample##
        sample= shapes.cylinder(radius=sample_Radius_str, height=sample_Height_str)
        return(sample)

    def clampcell_whole(self):
        """
                     creating clampcell geometry by joining all of the components together

                     Parameters
                     ----------
                     Returns
                     -------
                     geometry of the calampcell with sample: object
                     """
        return (operations.unite(operations.unite(self.outer_body(), self.inner_sleeve()), self.sample()))

    def creating_geometry_xml(self, objectGeo, fileNameTosave,patheNameTOSave, scad_flag ):
        """
                  creating the xml file of the clampcell geometry based on if the xml file will be
                  rendering to cad file or will be using to run the simulation
                  using mcvine

                  Parameters
                  ----------
                  objectGeo: object
                     the geometry of the body  of clampcell
                  fileNameTosave: string
                        name of the xml geometry file to be saved
                  patheNameTOSave: string
                        name of the path where the xml geometry file will be saved
                  scad_flag: boolen
                        to indicate if the xml file will be used to render cad file

                  Returns: object
                  -------
                  xml file of the object geometry
                  """
        renderin_the_file(objectGeo, fileNameTosave, patheNameTOSave, scad_flag)





