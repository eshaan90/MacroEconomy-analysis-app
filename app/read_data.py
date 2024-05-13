import pandas as pd
import os
import streamlit as st
import configparser
from pathlib import Path
#import json

thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'config.ini')

config = configparser.ConfigParser()
config.read(initfile)
MIN_YEAR = int(config.get('period', 'MIN_YEAR'))
MAX_YEAR = int(config.get('period', 'MAX_YEAR'))
DATAPATH=config.get('files', 'DATAPATH')
FILENAME=config.get('files', 'FILENAME')
groups=config.get('data','GROUPS')

GROUPS=groups.split(',')

@st.cache_data  # Add the caching decorator
def load_data(filepath, engine='openpyxl'):
    df=pd.read_excel(filepath ,engine=engine)
    return df

path = Path(__file__)
ROOT_DIR = path.parent.absolute()
filepath = os.path.join(ROOT_DIR, DATAPATH, FILENAME)
#print(filepath)
df=load_data(filepath)
