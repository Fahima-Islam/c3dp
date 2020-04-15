import pkgutil

DEFAULT_INSTRUMENT_CONFIGURATION  = pkgutil.get_loader("instruments/myinstrument_multipleDetectors").get_filename()
