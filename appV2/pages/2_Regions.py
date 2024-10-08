import streamlit as st
import pandas as pd
import altair as alt


#local
from read_data import df_regions,df_long,MIN_YEAR,MAX_YEAR
from visualize import plot_altair_line_chart

st.markdown("<h1 style='text-align: center;'>Regions: An Exploration</h1>", unsafe_allow_html=True)

regions=df_regions['name'].tolist()
selected_region=st.selectbox('Select a region',regions)
members=df_regions[df_regions['name']==selected_region]['members'].values[0]
members=members.split(',')

df_region=df_long[df_long['Country']==selected_region]
cols_to_keep=['Series','Year','Value']
df_region=df_region[cols_to_keep]
df_region=df_region.pivot(columns='Year',index='Series',values='Value')
df_region=df_region.dropna(how='all', ignore_index=False,inplace=False)
# st.header(selected_region)
tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Economy", "Compare","Data"])

with tab1:
    st.write(f"Total members: {len(members)}")

    # st.write(df_region)
    selected_year=st.slider('Select Year',MIN_YEAR,MAX_YEAR,step=1)

    col1,col2=st.columns([0.7,0.3])

    #Create folium map highlighting member countries



    series='GDP (current US$)'
    year='2009'
    chart_data=df_long[(df_long['Series']==series)&(df_long['economy'].isin(members))]

    col1.write(df_region)

    #Create GDP Percent of Total Bar Graph

    data=chart_data[chart_data['Year']==year]
    bar_chart=alt.Chart(chart_data,title=series).transform_joinaggregate(
        TotalValue='sum(Value)',
    ).transform_calculate(
        PercentOfTotal="datum.Value / datum.TotalValue"
    ).mark_bar().encode(
        alt.X('PercentOfTotal:Q',title='PercentOfTotal').axis(format='.0%'),
        y=alt.Y('Country',type='nominal',title=None).sort('-x'),
        tooltip=['PercentOfTotal:Q']
    )
    col2.altair_chart(bar_chart)

with tab2:
    # chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
    selection = alt.selection_point(fields=['Country'], bind='legend')
    # point_nearest = alt.selection_point(on='pointerover', nearest=True)
    chart=alt.Chart(chart_data).mark_line(point=True).encode(
            x='Year:T',
            y=alt.Y('Value',type='quantitative',title=None),
            # color=alt.condition(point_nearest, alt.Color('Country',type='nominal').legend(orient='bottom'), alt.value('lightgray')),
            color=alt.Color('Country',type='nominal').legend(orient='bottom'),
            opacity=alt.condition(selection, alt.value(0.8), alt.value(0.2)),
            tooltip=['Country','Year:T','Value']
            ).properties(
                height=500,
                width=700,
                title=series
            ).configure_axis(
                grid=True
            ).configure_view(
                stroke=None
            ).add_params(
                selection,
                # point_nearest
            ).interactive()

    chart.configure_title(
        fontSize=20,
        font='Courier',
        anchor='start',
        color='gray'
        )

    # st.write(chart_data)
    st.altair_chart(chart,use_container_width=True)

    series='GDP per capita (current US$)'
    chart_data=df_long[(df_long['Series']==series)&(df_long['economy'].isin(members))]
    # chart=plot_altair_line_chart(chart_data, 'Year','Value','temporal','quantitative','Year',series,series)
    # st.write(chart_data)
    selection = alt.selection_point(fields=['Country'], bind='legend')
    chart=alt.Chart(chart_data).mark_line(point=True).encode(
            x='Year:T',
            y=alt.Y('Value',type='quantitative',title=None),
            color=alt.Color('Country',type='nominal').legend(orient='bottom'),
            opacity=alt.condition(selection, alt.value(0.8), alt.value(0.2)),
            tooltip=['Country','Year:T','Value']
            ).properties(
                height=500,
                width=800,
                title=series
            ).configure_axis(
                grid=True
            ).configure_view(
                stroke=None
            ).add_params(
                selection
            ).interactive()

    chart.configure_title(
        fontSize=20,
        font='Courier',
        anchor='start',
        color='gray'
        )
    st.altair_chart(chart,use_container_width=True)
