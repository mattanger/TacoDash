import importlib
import os
import sys
from importlib.machinery  import SourceFileLoader
import logging
from dotenv import load_dotenv


logger = logging.getLogger(__name__)

load_dotenv()

DASHBOARD = {}

CONFIG_PATH_ENV_VAR = "TACODASH_CONFIG_PATH"
PID_LOCK_FILE = '/tmp/tacodash.pid'
ARTNET_UNIVERSE = 1

DEFAULT_FONT_NAME = 'ARIAL'

BACKGROUND_COLOR = (30, 19, 34)

STATUS_FILE = '/tmp/tacodash_status'

FULLSCREEN = bool(os.getenv('FULLSCREEN', False))

HEIGHT = 1600
WIDTH = 720
MODE = (HEIGHT, WIDTH)

if FULLSCREEN: 
    MODE = (0,0)


try:
    # pylint: disable=import-error,wildcard-import,unused-wildcard-import
    import dashboard_config 
    from dashboard_config import *  # type: ignore

    print(f"Loaded your LOCAL configuration at [{dashboard_config.__file__}]")
except Exception:
    logger.exception("Found but failed to import local dashboard_config")
    raise
