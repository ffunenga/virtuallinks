from .virtuallinks import Decorator

from .virtuallinks import set_debug
from .virtuallinks import list_registered
from .virtuallinks import nregistered

from .virtuallinks import enable_inspector
from .virtuallinks import disable_inspector

from .virtuallinks import ntypical
from .virtuallinks import monitor
from .virtuallinks import monitor_typical
from .virtuallinks import unmonitor
from .virtuallinks import unmonitor_typical
from .virtuallinks import unmonitor_all

from .virtuallinks import link
from .virtuallinks import unlink
from .virtuallinks import unlink_all
from .virtuallinks import nlinks


__name__ = 'virtuallinks'
__version__ = '0.0.1'
__author__ = 'Filipe Funenga'
__license__ = 'MIT'
__description__ = 'A simulator of file system links.'
