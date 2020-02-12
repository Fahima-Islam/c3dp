
import SCADGen.Parser

def xmlToOpenScad(filename='collimator_support_ed2.xml'):
    """converting .xml file to .scad file


         Parameters
         ----------
         filename: str
              name of the .xml file

         Returns
         -------
         .scad file
         """
    p=SCADGen.Parser.Parser(filename)
    p.createSCAD()
    test = p.rootelems[0]
