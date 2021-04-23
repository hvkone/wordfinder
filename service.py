# This module provides service functionality to app.py
# working directory is src folder.
import json
import sys
import os
import pandas as pd
import numpy as np
from typing import List
from sklearn.cluster import KMeans
from collections import defaultdict
from src.train.result_model import TResult
from src.train.store import StoreData
from src.util import *
from src.train.train_cluster import load_model
from src.train.train_model import UdpipeTrain
from src.train.cluster import Evaluator
from src.logs import Log
try:
    logger = Log()
    logger.info("begin to connect database")
    store_data = StoreData(db_config['user'],
                           db_config['password'],
                           db_host=db_config['db_host'],
                           db_name=db_config['db_name'])
    cnx = store_data.db_connect()
    logger.info("succeed to connect database")
    cursor = cnx.cursor()
except Exception as ex:
    logger.error('logging in database error %s' % ex)