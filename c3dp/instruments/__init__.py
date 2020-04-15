import pkgutil

DEFAULT_INSTRUMENT_CONFIGURATION  = pkgutil.get_loader("c3dp/instruments/myinstrument_multipleDetectors").get_filename()
