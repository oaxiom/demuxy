"""
config.py

"""

import os, logging

# -------------- Versioning data

version = "0.9"
__version__ = version 
        
# set-up logging
logging.basicConfig(level=logging.INFO,
                    format='%(levelname)-8s: %(message)s',
                    datefmt='%m-%d %H:%M')
log = logging.getLogger('prefunchip')

# -------------- General options

