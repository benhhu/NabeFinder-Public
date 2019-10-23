from flask import Flask
import json
import os
import xgboost as xgb
import MySQLdb as mdb
import pandas as pd 
import geopandas as gpd
app = Flask(__name__)
from app import views

