import pandas as pd
import os
import streamlit as st
import configparser
#import json


config = configparser.ConfigParser()
config.read('config.ini')
MIN_YEAR = int(config.get('period', 'MIN_YEAR'))
MAX_YEAR = int(config.get('period', 'MAX_YEAR'))
DATAPATH=config.get('files', 'DATAPATH')
FILENAME=config.get('files', 'FILENAME')
groups=config.get('data','GROUPS')

GROUPS=groups.split(',')

@st.cache_data  # 👈 Add the caching decorator
def load_data(filepath, engine='openpyxl'):
    df=pd.read_excel(filepath ,engine=engine)
    return df

filepath=os.path.join(DATAPATH,FILENAME)
df=load_data(filepath)
