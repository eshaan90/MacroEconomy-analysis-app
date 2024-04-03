import streamlit as st
import plotly.express as px
import numpy as np
from read_data import df,MIN_YEAR,MAX_YEAR,GROUPS

st.title('World Economics')
num_cols=np.arange(MIN_YEAR, MAX_YEAR)
#st.write(GROUPS)

df=df[~df['Country/Group Name'].isin(GROUPS)]
subjects=df['Subject'].unique()
subject=st.selectbox('Choose subject',subjects)
df_tmp=df[df['Subject']==subject]
#df_tmp=df_tmp[~df_tmp['Country/Group Name'].isin(GROUPS)]
selected_year=st.select_slider("Select Year", options=num_cols) 

#df_tmp[selected_year]=df_tmp[selected_year].astype(np.float16)
df_tmp=df_tmp.sort_values(by=selected_year,axis=0,ascending=False)
display_row_count=30
df_tmp=df_tmp.iloc[:display_row_count][:]

fig = px.bar(df_tmp, x=selected_year, y='Country/Group Name',
            title=subject, orientation='h')
st.plotly_chart(fig, use_container_width=True)

#Show data
st.title('Data:')
st.dataframe(df_tmp, use_container_width=True)