
import pandas as pd
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

#local
from read_data import df,MIN_YEAR,MAX_YEAR


st.title('Comparative Analysis')


countries=df['Country/Group Name'].unique()
subjects=df['Subject'].unique()
country=st.multiselect('Choose countries/economic groups',countries)
subject=st.selectbox('Choose subject',subjects)
df_tmp=df[(df['Country/Group Name'].isin(country)) & (df['Subject']==subject)]
# units=df_tmp['Units'].unique()
# unit=st.selectbox('Select Unit',units)
# df_tmp=df_tmp[df_tmp['Units']==unit]
scale=df_tmp.iloc[0]['Scale']
if st.button('Plot'):
    #estimate_year=int(df_tmp.loc[df_tmp.index[0],'Estimates Start After'])

    num_cols=np.arange(MIN_YEAR, MAX_YEAR).tolist()
    cols_to_keep=['Country/Group Name']+ num_cols
    df_tmp=df_tmp[cols_to_keep]

    df_tmp=df_tmp.rename({'Country/Group Name':''},axis=1)
    df_tmp=df_tmp.set_index('')
    df_tmp=df_tmp.T.reset_index()
    df_tmp=df_tmp.rename({'index':'Year'},axis=1)

    # matplotlib plot
    # fig=plt.figure()#figsize=(15,6))
    # for c in country:
    #     plt.plot(df_tmp['Year'],df_tmp[c],'.-',label=c)

    # plt.title(subject +' (in '+unit+')')
    # plt.axvline(x = estimate_year, ymin = 0.05, ymax = 0.95, color = 'purple', drawstyle='steps',linestyle='dashed')
    # plt.legend(loc='upper left')

    #plotly plot
    fig = go.Figure()
    for c in country:
        fig.add_trace(go.Scatter(x=df_tmp['Year'], y=df_tmp[c],
                    name=c))
        
    # Edit the layout
    fig.update_traces(hoverinfo='all', mode='lines+markers')
    fig.update_layout(title=subject+' (in '+ scale+')',
                   xaxis_title='Year',
                   yaxis_title=subject)

    st.plotly_chart(fig, use_container_width=True)

    #Show data
    st.title('Data:')
    st.write(df_tmp)