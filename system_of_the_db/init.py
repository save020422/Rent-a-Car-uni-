# system_of_the_db/init.py
import sys
import os


from .consructor import *

db = SystemOfDb()
info_manager = InfoManager(db)
