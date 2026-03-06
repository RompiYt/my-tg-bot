import logging
import sys

def setup_logging():
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
