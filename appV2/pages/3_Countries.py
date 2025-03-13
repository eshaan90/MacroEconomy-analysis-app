import streamlit as st
st.set_page_config(page_title='Countries',layout="wide")
import os
import pandas as pd
import numpy as np
import altair as alt
from numerize import numerize 
from datetime import datetime
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
#local
from read_data import df_long,MIN_YEAR,MAX_YEAR,df_economies,DATAPATH,RAW,FLAGS_FOLDERNAME
from visualize import plot_altair_line_chart, plot_altair_bar_chart,plot_altair_bar_chart_with_mean

pd.options.display.float_format = '{:,.2f}'.format
def section_expander(flag):
    if flag:
        return st.sidebar.button('Collapse All Sections',type='primary')
    else: 
        return st.sidebar.button('Expand All Sections',type='primary')

countries=df_long.Country.unique().tolist()
all_series=df_long.Series.unique().tolist()

st.sidebar.title('1. Data')
data_container=st.sidebar.container(border=True)
selected_country=data_container.selectbox('Select a country',countries, index=10, placeholder="Choose an option")
# selected_year=st.slider('Select Year',MIN_YEAR,MAX_YEAR,step=1)
time_range = data_container.slider(
    "Select Year Range",min_value=MIN_YEAR,max_value=datetime.now().year,
    value=(1980, datetime.now().year)
    )

col1,col2=st.columns([.8,.2],gap='large')
col1.title(f'Country: {selected_country}')
# st.write(os.getcwd())
iso2=df_economies.loc[df_economies['name']==selected_country]['ISO2'].values[0]
flag_img_path=os.path.join('assets',RAW,FLAGS_FOLDERNAME,iso2.lower()+'.png')
fig,ax=plt.subplots(figsize=(.8,1))
# Read the image
img = mpimg.imread(flag_img_path)

# Display the image
im=ax.imshow(img)
ax.axis('off')  # Optional: Turn off axis labels
col2.pyplot(fig,use_container_width=False)

# st.info('This is a purely informational message', icon="ℹ️")

section_expander_flag=True
# section_expander_flag=section_expander(section_expander_flag)
st.sidebar.title('2. Compare')

with st.sidebar.expander('Compare Economies',expanded=False):
    additional_countries=st.multiselect(label='Select countries',options=countries, placeholder="Choose multiple countries",max_selections=9)
    compare_ecos=st.button('Compare',key='compare_ecos')

with st.sidebar.expander('Compare Time Periods',expanded=False):
    event1=st.text_input('Event Name:',value='Event 1',placeholder='Give a custom event name')
    event1_time_period = st.slider( "Select Event 1 Time Period",min_value=MIN_YEAR,max_value=MAX_YEAR,
    value=(2000, 2010)
    )
    event2=st.text_input('Event Name:',value='Event 2',placeholder='Give a custom event name')
    event2_time_period = st.slider( "Select Event 2 Time Period",min_value=MIN_YEAR,max_value=MAX_YEAR,
    value=(2011, 2020)
    )
    compare_tp=st.button('Compare',key='compare_tps')

events_df=pd.DataFrame()
if compare_tp:
    events=[{'start':str(event1_time_period[0]),'end':str(event1_time_period[1]),'event':event1},
            {'start':str(event2_time_period[0]),'end':str(event2_time_period[1]),'event':event2},
            # {'start':event3_time_period[0],'end':event3_time_period[1],'event':event3}
    ]
    events_df=pd.DataFrame(events)
# st.write(events_df)
mainTab1, mainTab2, mainTab3, mainTab4 = st.tabs(["Overview", "Economy", "Compare","Data"])
years=np.arange(time_range[0],time_range[1],1)
years_str=[str(year) for year in years]

if compare_ecos:
    additional_countries.append(selected_country)
    selected_data=df_long[(df_long['Country'].isin(additional_countries))&(df_long['Year'].isin(years_str))]
else:
    selected_data=df_long[(df_long['Country']==selected_country)&(df_long['Year'].isin(years_str))]
# st.write(selected_data)

with mainTab1:
    c9,c10=st.columns(2)
    c11,c12=st.columns(2)

    with c9:
        tab1, tab2 = st.tabs(["Line", "Bar"])
        series='Population, total'
        chart_data=selected_data[(selected_data['Series']==series)]
        with tab1:
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)
            st.altair_chart(chart,use_container_width=True)
        with tab2:
            chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
            st.altair_chart(chart,use_container_width=True)
    
    with c10:
        pass
        # series='GDP (current US$)'
        # chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
        # chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
        # # st.write(chart_data)
        # st.altair_chart(chart)
    with c11:
        tab1, tab2 = st.tabs(["Line", "Bar"])
        series='Population density (people per sq. km of land area)'
        chart_data=selected_data[(selected_data['Series']==series)]
        with tab1:
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)
            st.altair_chart(chart,use_container_width=True)
        with tab2:
            chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
            st.altair_chart(chart,use_container_width=True)

with mainTab2:
    with st.expander(":green[**GDP**]",expanded=section_expander_flag):
        c1,c2=st.columns(2)
        c3,c4=st.columns(2)

        with c1:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series='GDP (current US$)'
            chart_data=selected_data[(selected_data['Series']==series)]
            # st.write(chart_data)
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)
        with c2:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series='GDP growth (annual %)'
            chart_data=selected_data[(selected_data['Series']==series)]
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)

        with c3:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series='GDP per capita (current US$)'
            chart_data=selected_data[(selected_data['Series']==series)]
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)

        with c4:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series='GDP per capita growth (annual %)'
            chart_data=selected_data[(selected_data['Series']==series)]
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)
        
    with st.expander(":green[**DEBT**]",expanded=section_expander_flag):
    # st.write("## 2. Debt")
        c5,c6=st.columns(2)
        c7,c8=st.columns(2)    
        with c5:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series='Central government debt, total (% of GDP)'
            chart_data=selected_data[(selected_data['Series']==series)]
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)

        with c6:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series='Interest payments (% of revenue)'
            chart_data=selected_data[(selected_data['Series']==series)]
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)

        with c7:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series='Current account balance (% of GDP)'
            chart_data=selected_data[(selected_data['Series']==series)]
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)

        with c8:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series='Total Reserves (% of total external debt)'
            chart_data=selected_data[(selected_data['Series']==series)]
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)

    with st.expander(":green[**INFLATION**]",expanded=section_expander_flag):
        tab1, tab2 = st.tabs(["Line", "Bar"])
        series='Inflation, consumer prices (annual %)'
        chart_data=selected_data[(selected_data['Series']==series)]
        with tab1:
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
            st.altair_chart(chart,use_container_width=True)
        with tab2:
            chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
            st.altair_chart(chart,use_container_width=True)


    with st.expander(":green[**UNEMPLOYMENT**]",expanded=section_expander_flag):
        c9,c10=st.columns(2)
        with c9:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series=['Unemployment, total (% of total labor force) (national estimate)',
                    # 'Unemployment, total (% of total labor force) (modeled ILO estimate)'
                    ]
            chart_data=selected_data[selected_data['Series']==series[0]]
            title='Unemployment (% of total labor force)'
            # legend_values=['National Estimate',
            #                 'Modeled ILO Estimate']
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,title)        
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,title)
                st.altair_chart(chart,use_container_width=True)
        with c10:
            tab1, tab2 = st.tabs(["Line", "Bar"])
            series='Gini index'
            chart_data=selected_data[selected_data['Series']==series]
            with tab1:
                chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
                st.altair_chart(chart,use_container_width=True)
            with tab2:
                chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
                st.altair_chart(chart,use_container_width=True)


    with st.expander(":green[**INTEREST RATE**]",expanded=section_expander_flag):
        tab1, tab2 = st.tabs(["Line", "Bar"])
        series='Real interest rate (%)'
        chart_data=selected_data[selected_data['Series']==series]
        with tab1:
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative',events_df,'Year',series,series)        
            st.altair_chart(chart,use_container_width=True)
        with tab2:
            chart=plot_altair_bar_chart_with_mean(chart_data, 'Year','Value','nominal','quantitative',events_df,'Year',series,series)
            st.altair_chart(chart,use_container_width=True)

with mainTab3:
    # select_countries=st.multiselect("Choose countries to Compare with:",countries,)
    con1=st.container()
    
    # with con1:
    #     selected_series1=st.selectbox('Choose Series:',all_series,key='con1')
    #     chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
    #     st.area_chart(chart_data)
    # con2=st.container()
    # with con2:
    #     selected_series2=st.selectbox('Select Series:',all_series,key='con2')
    #     chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
    #     st.area_chart(chart_data)
    #[Country Size, Population, GDP, Debt, Inflation, Unemployment, Gini Index]

with mainTab4:
    if selected_country:
        # ds_data=df_long[df_long['Country']==selected_country]
        st.write(selected_data)
    else:
        st.write(df_long)
