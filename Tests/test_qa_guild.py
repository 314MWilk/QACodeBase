import math
import os
import random
import re
from pathlib import Path

from Engine.CoreFiles.browser_settings import get_driver_config
from Engine.QAGuild.open_page import OpenLeoCode

cwd = Path(__file__).parents[1]
os.chdir(str(cwd))
driver_config = get_driver_config()


def test_everything_here():
    print(random.random()*10)
    # with OpenLeoCode(driver_config) as home:
    #     blog = home.click_on_blog()
    #     home.home()
