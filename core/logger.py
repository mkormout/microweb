import ulogging as logging
from ulogging import NOTSET, DEBUG, INFO, WARNING, ERROR, CRITICAL

debug_enabled = True

logger = logging.getLogger('microweb')

logger.level = DEBUG if debug_enabled else INFO
