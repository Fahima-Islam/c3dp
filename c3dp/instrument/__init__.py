import pkgutil

DEFAULT_INSTRUMENT_CONFIGURATION  = pkgutil.get_loader("c3dp.instrument.myinstrument").get_filename()
