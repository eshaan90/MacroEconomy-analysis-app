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
EDA=config.get('files', 'EDA')
FILENAME=config.get('files', 'FILENAME')
REGIONS_FILENAME=config.get('files','REGIONS_FILENAME')

# GROUPS=groups.split(',')

@st.cache_data  # Add the caching decorator
def load_data(filepath, filetype, engine='openpyxl'):
    if filetype=='csv':
        df=pd.read_csv(filepath)
    elif filetype=='excel':
        df=pd.read_excel(filepath ,engine=engine)
    else:
        df=None
    return df

path = Path(__file__)
ROOT_DIR = path.parent.absolute()
filepath = os.path.join(ROOT_DIR, DATAPATH, EDA, FILENAME)
df=load_data(filepath,'csv')

df_long=df.melt(id_vars=["economy", "Country","series","Series"],\
        var_name="Year",
        value_name="Value")

filepath = os.path.join(ROOT_DIR, DATAPATH, EDA, REGIONS_FILENAME)
df_regions=load_data(filepath,'csv')

