import streamlit as st
st.set_page_config(page_title='Countries',layout="wide")

import pandas as pd
import numpy as np
import altair as alt
from numerize import numerize 

#local
from read_data import df_long,MIN_YEAR,MAX_YEAR
from visualize import plot_altair_line_chart

pd.options.display.float_format = '{:,.2f}'.format

st.title('PROFILING COUNTRIES')
countries=df_long.Country.unique().tolist()
all_series=df_long.Series.unique().tolist()
selected_country=st.selectbox('Select a country',countries, index=None, placeholder="Choose an option")
# selected_year=st.slider('Select Year',MIN_YEAR,MAX_YEAR,step=1)
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Economy", "Compare","Data"])


with tab1:
    c9,c10=st.columns(2)
    c11,c12=st.columns(2)

    with c9:
        series='Population, total'
        chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
        chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
        # st.write(chart_data)
        st.altair_chart(chart)
    
    with c10:
        pass
        # series='GDP (current US$)'
        # chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
        # chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
        # # st.write(chart_data)
        # st.altair_chart(chart)
    with c11:
        series='Population density (people per sq. km of land area)'
        chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
        chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
        # st.write(chart_data)
        st.altair_chart(chart)

with tab2:
    with st.expander(":green[**GDP**]",expanded=True):
        # st.write("## 1. GDP")
        c1,c2=st.columns(2)
        c3,c4=st.columns(2)

        with c1:
            series='GDP (current US$)'
            chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
            # st.write(chart_data)
            st.altair_chart(chart)

        with c2:
            series='GDP growth (annual %)'
            chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
            
            st.altair_chart(chart)

        with c3:
            series='GDP per capita (current US$)'
            chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
            
            st.altair_chart(chart)
        with c4:
            series='GDP per capita growth (annual %)'
            chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
            
            st.altair_chart(chart)
        
    with st.expander(":green[**DEBT**]",expanded=True):
    # st.write("## 2. Debt")
        c5,c6=st.columns(2)
        c7,c8=st.columns(2)    
        with c5:
            series='Central government debt, total (% of GDP)'
            chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)

            st.altair_chart(chart,use_container_width=True)
        with c6:
            series='Interest payments (% of revenue)'
            chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)

            st.altair_chart(chart,use_container_width=True)

        with c7:
            series='Current account balance (% of GDP)'
            chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
            chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)

            st.altair_chart(chart,use_container_width=True)

    with st.expander(":green[**INFLATION**]",expanded=True):
        # st.write("## 3. Inflation")
        # with c5:
        series='Inflation, consumer prices (annual %)'
        chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
        chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
        # st.write(chart_data)
        st.altair_chart(chart,use_container_width=True)

    with st.expander(":green[**UNEMPLOYMENT**]",expanded=True):
        # st.write("## 4. Unemployment")
        # with c6:
        series=['Unemployment, total (% of total labor force) (national estimate)',
                # 'Unemployment, total (% of total labor force) (modeled ILO estimate)'
                ]
        chart_data=df_long[(df_long['Series']==series[0])&(df_long['Country']==selected_country)]
        legend_values=['National Estimate',
                        'Modeled ILO Estimate']
        chart= alt.Chart(chart_data).mark_line(point=True).encode(
                x='Year:T',
                y=alt.Y('Value',type='quantitative',title='Unemployment (% of total labor force)'),
                # color=alt.Color('Series').legend(orient="bottom",title="Series",values=legend_values)
                ).properties(
                    # height=300,
                    # width=500,
                    title='Unemployment, total (% of total labor force)'
                ).configure_axis(
                    grid=True
                ).configure_view(
                    stroke=None
                ).interactive()

        chart.configure_title(
            fontSize=20,
            font='Courier',
            anchor='start',
            color='gray'
        )
        # plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
        
        st.altair_chart(chart,use_container_width=True)

    with st.expander(":green[**INTEREST RATE**]",expanded=True):
        # st.write("## 5. Interest Rate")
        series='Real interest rate (%)'
        chart_data=df_long[(df_long['Series']==series)&(df_long['Country']==selected_country)]
        chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
        # st.write(chart_data)
        st.altair_chart(chart,use_container_width=True)

with tab3:
    select_countries=st.multiselect("Choose countries to Compare with:",countries,)
    con1=st.container()
    
    with con1:
        selected_series1=st.selectbox('Choose Series:',all_series,key='con1')
        chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
        st.area_chart(chart_data)
    con2=st.container()
    with con2:
        selected_series2=st.selectbox('Select Series:',all_series,key='con2')
        chart_data = pd.DataFrame(np.random.randn(20, 3),columns=['a', 'b', 'c'])
        st.area_chart(chart_data)
with tab4:
    if selected_country:
        ds_data=df_long[df_long['Country']==selected_country]
        st.write(ds_data)
    else:
        st.write(df_long)
