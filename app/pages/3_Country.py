import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#local
from read_data import df,MIN_YEAR,MAX_YEAR


def plotly_linechart(df,country,subject,scale=''):
    """
    Plot line chart using plotly
    """
    if scale:
        yaxis_title=subject+' (in '+ scale+')'
    else:
        yaxis_title=subject


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[country], name=subject))
        
    # Edit the layout
    fig.update_traces(hoverinfo='all', mode='lines+markers')

    fig.update_layout(xaxis_title='Year', yaxis_title=yaxis_title)
    st.plotly_chart(fig, use_container_width=True)


st.title('MacroEconomics of a Country')

num_cols=np.arange(MIN_YEAR, MAX_YEAR)

tab1,tab2=st.tabs(['Country/Group','Comparing Subjects/Countries'])

countries=df['Country/Group Name'].unique()

with tab1:
    country=st.selectbox('Select a country/economic group',countries,index=186)
    df_tmp=df[df['Country/Group Name']==country]
    subjects=df_tmp['Subject'].unique()
    min_year, max_year = st.select_slider('Select Year Range',num_cols,(MIN_YEAR, 2023))

    cols_to_keep=['Country/Group Name','Subject','Scale']+ num_cols.tolist()
    df_tmp=df_tmp[cols_to_keep]
    #df=df.rename({'Country':''},axis=1)
    df_tmp=df_tmp.set_index('Country/Group Name')
    #estimate_year=int(df_tmp.loc[df_tmp.index[0],'Estimates Start After'])


    container1=st.container(border=False)

    col1,col2,col3 = container1.columns(3)


    with col1:
        subject=st.selectbox('Subject',subjects,index=1,key=1)
        df_tmp=df_tmp[df_tmp['Subject']==subject]
        scale=df_tmp.iloc[0]['Scale']

        #units=df_tmp['Units'].unique()
        #unit=st.selectbox('Unit',units,index=1,key=2)

        #df_tmp=df_tmp[df_tmp['Units']==unit]
        df_tmp=df_tmp[num_cols]
        df_tmp.columns.names = ['Year']
        df_tmp=df_tmp.T
        df_tmp=df_tmp.loc[min_year:max_year]

        #st.write(df_tmp)
        

        plotly_linechart(df_tmp, country,subject,scale)

        
    with col2:
        subject2=st.selectbox('Subject',subjects,index=5, key=3)
        df_tmp=df_tmp[df_tmp['Subject']==subject2]
        # units=df_tmp['Units'].unique()
        # unit2=st.selectbox('Unit',units,index=0,key=4)
        # df_tmp=df_tmp[df_tmp['Units']==unit2]

        df_tmp=df_tmp[num_cols]
        df_tmp.columns.names = ['Year']
        df_tmp=df_tmp.T
        df_tmp=df_tmp.loc[min_year:max_year]

        plotly_linechart(df_tmp, country,subject2)

    with col3:
        subject2=st.selectbox('Subject',subjects,index=10,key=5)
        df_tmp=df_tmp[df_tmp['Subject']==subject2]
        # units=df_tmp['Units'].unique()
        # unit2=st.selectbox('Unit',units,index=0,key=6)
        # df_tmp=df_tmp[df_tmp['Units']==unit2]

        df_tmp=df_tmp[num_cols]
        df_tmp.columns.names = ['Year']
        df_tmp=df_tmp.T
        df_tmp=df_tmp.loc[min_year:max_year]

        plotly_linechart(df_tmp, country,subject2)


    container2=st.container(border=False)

    col1,col2,col3 = container2.columns(3)


    with col1:
        subject=st.selectbox('Subject',subjects,index=8,key=7)
        df_tmp=df_tmp[df_tmp['Subject']==subject]
        # units=df_tmp['Units'].unique()
        # unit=st.selectbox('Unit',units,key=8)
        # df_tmp=df_tmp[df_tmp['Units']==unit]


        df_tmp=df_tmp[num_cols]
        df_tmp.columns.names = ['Year']
        df_tmp=df_tmp.T
        df_tmp=df_tmp.loc[min_year:max_year]

        plotly_linechart(df_tmp, country,subject)

        
    with col2:
        subject2=st.selectbox('Subject',subjects,index=9,key=9)
        df_tmp=df_tmp[df_tmp['Subject']==subject2]
        # units=df_tmp['Units'].unique()
        # unit2=st.selectbox('Unit',units,key=10)
        # df_tmp=df_tmp[df_tmp['Units']==unit2]

        df_tmp=df_tmp[num_cols]
        df_tmp.columns.names = ['Year']
        df_tmp=df_tmp.T
        df_tmp=df_tmp.loc[min_year:max_year]

        plotly_linechart(df_tmp, country,subject2)

    with col3:
        subject2=st.selectbox('Subject',subjects,index=27,key=11)
        df_tmp=df_tmp[df_tmp['Subject']==subject2]
        # units=df_tmp['Units'].unique()
        # unit2=st.selectbox('Unit',units,index=1,key=12)
        # df_tmp=df_tmp[df_tmp['Units']==unit2]

        df_tmp=df_tmp[num_cols]
        df_tmp.columns.names = ['Year']
        df_tmp=df_tmp.T
        df_tmp=df_tmp.loc[min_year:max_year]

        plotly_linechart(df_tmp, country,subject2)


    st.title('Data')
    st.write(df)

with tab2:
    st.write(df.columns)
    country=st.multiselect('Choose countries/economic groups',countries)
    df_tmp=df[df['Country/Group Name'].isin(country)]
    subjects=df_tmp['Subject'].unique()
    sel_subjects=st.multiselect('Choose subjects',subjects)
    df_tmp=df_tmp[(df_tmp['Subject'].isin(sel_subjects))]
    min_year, max_year = st.select_slider('Select Year Range',num_cols,(MIN_YEAR, 2023))

    cols_to_keep=['Country/Group Name','Subject','Scale']+ num_cols.tolist()
    df_tmp=df_tmp[cols_to_keep]
    df_tmp=df_tmp.set_index('Country/Group Name')