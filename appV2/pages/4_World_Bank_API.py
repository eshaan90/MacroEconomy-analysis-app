import streamlit as st
import wbgapi as wb
import pandas as pd
import numpy as np
from datetime import datetime
import altair as alt
from read_data import MIN_YEAR,MAX_YEAR

# st.set_page_config(page_title='World Bank API',
#                    layout="wide"
#     )

@st.cache_data(persist="disk")
def get_series_info(q):
    try:
        if q:
            data=wb.series.Series(q=q)
        else:
            data=wb.series.Series()
    except Exception as e:
        print(f"Error: {e}")
    return data

@st.cache_data(persist="disk")
def get_economies():
    return wb.economy.DataFrame(id='all',labels=True,skipAggs=False)
    
@st.cache_data(persist="disk")
def get_data(series,economy,time_range):
    try:
        data = wb.data.DataFrame(selected_series, economy=economy_codes,time=range(time_range[0],time_range[1]),
                        skipAggs=False, labels=True, numericTimeKeys=True, timeColumns=True)
    except Exception as e:
        data=None
        st.error(f'Connection Error: Unable to access World Bank API', icon="🚨")
    return data

st.markdown("<h1 style='text-align: center;'>Explore World Bank Series</h1>", unsafe_allow_html=True)

st.info("""
        Use the Search bar below to find a series from the World Bank DataSet.\n
        Visualize the same by selecting the series and from the sidebar, select the countries and year range.
        """)

# st.title("Explore World Bank Series")
q=st.text_input(label='1.Enter a string to Search',placeholder='Inflation')
col1, col2 = st.columns([.6, .4],vertical_alignment="top")

data=get_series_info(q)
data=data.to_frame(name='Series Name').reset_index().rename({'index':'Series ID'},axis=1)
data=data[['Series Name','Series ID']]


event=col2.dataframe(data=data[['Series Name']],use_container_width=True, hide_index=True,
             on_select="rerun", selection_mode="single-row")

# col2.write("Choose a series from the table above to visualize its data below (Click on the leftmost column for selection)")

# col1.header('Visualizing a Series')

df_economies=get_economies()
economies=df_economies.name.tolist()
selected_economies=st.sidebar.multiselect(label='2.Select countries/regions',options=economies,default='United States',max_selections=9)

time_range = st.sidebar.slider(
    "3.Select Data Range",min_value=MIN_YEAR,max_value=datetime.now().year,
    value=(1980, datetime.now().year)
    )

tab1, tab2 = col1.tabs(["Line", "Bar"])


if st.sidebar.button('Plot series'):
    if event.selection['rows']:
        selected_series=data.iloc[event.selection['rows'][0]]['Series ID']
        selected_series_name=data.iloc[event.selection['rows'][0]]['Series Name']
        # col1.write(f"Selected Series: {selected_series}")
        # col1.write(f"Series name: {selected_series_name}")
    if selected_economies:
        economy_codes=df_economies[df_economies['name'].isin(selected_economies)].index.values
        # col1.write(f"Selected economies: {economy_codes}")
    # col1.write(f"Selected time range for: {time_range}")

    if event.selection['rows'] and selected_economies:
        df=get_data(selected_series, selected_economies, time_range)
        
        #plot the data
        if df is not None:
            timePeriod=np.arange(time_range[0],time_range[1])
            chart_data=df.dropna(how='all', subset=timePeriod, \
                            ignore_index=False,inplace=False)
            available_countries=chart_data['Country'].tolist()

            chart_data.reset_index(drop=True,inplace=True)

            chart_data=chart_data.melt(id_vars=["Country"],
                                var_name="Year",
                                value_name="Value")
            # st.write(chart_data.dtypes)
            chart_data['Year']=chart_data['Year'].astype('string')
            # st.write(chart_data.select_dtypes("string"))

            selection = alt.selection_point(fields=['Country'], bind='legend')
            brush=alt.selection_interval(encodings=['x'],bind='scales')
            line_chart=alt.Chart(chart_data,title=alt.Title(selected_series_name,
                                                       subtitle=selected_series)
                                                       ).mark_line(point=True).encode(
                    x='Year:T',
                    y=alt.Y('Value',type='quantitative',title=None),
                    color=alt.condition(brush, alt.Color('Country:N').legend(orient='bottom'), alt.value('lightgray')),
                    strokeOpacity=alt.condition(selection, alt.value(0.9), alt.value(0.1)),
                    tooltip=['Year:T','Country:N','Value:Q']
                    ).properties(
                        height=500,
                        width=300
                    ).add_params(
                        selection,
                        brush
                        )#.interactive()
            
            line_chart.configure_title(
                fontSize=20,
                font='Courier',
                anchor='start',
                color='gray',
                subtitleFont='Courier',
                subtitleColor='gray'
            )
            brush=alt.selection_interval(encodings=['x'],bind='scales')
            bar_chart=alt.Chart(chart_data,title=alt.Title(selected_series_name,
                                                       subtitle=selected_series)
                                                       ).mark_bar().encode(
                x=alt.X('Year:O',timeUnit='year',title='Year'),
                y=alt.Y('Value:Q',stack=None,title=None),
                xOffset="Country:N",
                color=alt.Color('Country:N').legend(orient='bottom'),
                # column=alt.Column('Country:N',align='each',center=True),
                
                tooltip=['Year:T','Country:N','Value:Q']
            ).properties(
                height=500,
                width=300
            ).add_params(
                        # selection,
                        brush
            )#.interactive()

            tab1.altair_chart(line_chart, use_container_width=True)
            tab2.altair_chart(bar_chart,use_container_width=True)

            with st.expander("See Data"):
                st.write(chart_data)
            
        
