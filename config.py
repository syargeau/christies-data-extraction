"""
Project configuration file.

Extract environment variables to be used as global constants
in the rest of the project.
"""

import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

URL_NOV_2017_SALE = os.getenv('URL_NOV_2017_SALE')
URL_MAR_2018_SALE = os.getenv('URL_MAR_2018_SALE')
