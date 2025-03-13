import streamlit as st
import pandas as pd
import os
import plotly.graph_objects as go
# from streamlit_option_menu import option_menu
from numerize import numerize

st.set_page_config(page_title="World Economics", layout="wide")

#local
from read_data import df_long,MIN_YEAR,MAX_YEAR
# from visualize import plot_altair_line_chart


st.title(f':green[World] Through the MacroEconomic Lens')
st.info(f'This app provides visual and statistical tools to help analyze, compare, and contrast  the world\'s economies. Data is sourced from World Bank and ranges from :red[{MIN_YEAR}] to :red[{MAX_YEAR}]')


economy='WLD'
df_world=df_long[df_long['economy']==economy]
cols_to_keep=['Series','Year','Value']
df_world=df_world[cols_to_keep]

df_world=df_world.pivot(columns='Series',index='Year',values='Value')
chart_data=df_world.dropna(axis=1,how='all', ignore_index=False,inplace=False)
# chart_data.reset_index(inplace=True)

# year=2022
# st.write(chart_data)

col1, col2, col3, col4, col5 = st.columns(5)

color='black'#'#ff0066'
col1.markdown(
            f"<p style='color: {color}; "
            f"font-weight: bold; font-size: 20px;'>Population</p>",
            unsafe_allow_html=True,
        )
col1.write(numerize.numerize(chart_data.loc['2022','Population, total'],4))

col2.markdown(
            f"<p style='color: {color}; "
            f"font-weight: bold; font-size: 20px;'>Land Area (sq. km)</p>",
            unsafe_allow_html=True,
        )
col2.write(numerize.numerize(chart_data.loc['2021','Land area (sq. km)'],4))

col3.markdown(
            f"<p style='color: {color}; "
            f"font-weight: bold; font-size: 20px;'>Population Density</p>",
            unsafe_allow_html=True,
        )
col3.write(numerize.numerize(chart_data.loc['2021','Population density (people per sq. km of land area)'],5))


col4.markdown(
            f"<p style='color: {color}; "
            f"font-weight: bold; font-size: 20px;'> GDP (current US$)</p>",
            unsafe_allow_html=True,
        )
col4.write(numerize.numerize(chart_data.loc['2022','GDP (current US$)'],4))


col5.markdown(
            f"<p style='color: {color}; "
            f"font-weight: bold; font-size: 20px;'> GDP per capita</p>",
            unsafe_allow_html=True,
        )
col5.write(numerize.numerize(chart_data.loc['2022','GDP per capita (current US$)'],7))

latitude = -22.2974
longitude = -46.6062

'''
#making the geo-plot
fig = go.Figure(go.Scattergeo(lat=[latitude], lon=[longitude])) #if you are passing just one lat and lon, put it within "[]""

#editing the marker
# fig.update_traces(marker_size=20, line=dict(color='Red'))

# this projection_type = 'orthographic is the projection which return 3d globe map'
# fig.update_geos(projection_type="natural earth2") 

#layout, exporting html and showing the plot
fig.update_layout(width= 600, height=600, margin={"r":0,"t":0,"l":0,"b":0},
                 geo = dict(
                        showland = True,
                        showcountries = True,
                        showocean = True,
                        showrivers=True,
                        countrywidth = 0.5,
                        landcolor = 'rgb(230, 145, 56)',
                        lakecolor = 'rgb(0, 255, 255)',
                        oceancolor = '#3399FF',#'rgb(0, 255, 255)',
                        projection = dict(
                            type = 'orthographic',
                            rotation = dict(
                                lon = -100,
                                lat = 40,
                                roll = 0
                            )
                        ),
                        lonaxis = dict(
                            showgrid = True,
                            gridcolor = 'rgb(102, 102, 102)',
                            gridwidth = 0.5
                        ),
                        lataxis = dict(
                            showgrid = True,
                            gridcolor = 'rgb(102, 102, 102)',
                            gridwidth = 0.5
                        )
                    )
            )
# fig.write_html("3d_plot.html")
# fig.show()
st.plotly_chart(fig, use_container_width=True)
'''

# with st.sidebar:
#     selected = option_menu(
#     menu_title = "Main Menu",
#     options = ["Home","World","Regions","Countries","World Bank API"],
#     icons = ["house","globe2","globe-europe-africa","activity","building"],
#     menu_icon = "cast",
#     default_index = 0,
#     #orientation = "horizontal",
# )
