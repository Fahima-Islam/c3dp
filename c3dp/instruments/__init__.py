import pkgutil
import os
this_dir = os.path.dirname(__file__)
myistrument_dir = os.path.join (this_dir,'myinstrument_multipleDetectors' )
DEFAULT_INSTRUMENT_CONFIGURATION  = pkgutil.get_loader(myistrument_dir).get_filename()
