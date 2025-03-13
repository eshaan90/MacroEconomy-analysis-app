import streamlit as st
import pandas as pd
import altair as alt


#local
from read_data import df_regions,df_long,MIN_YEAR,MAX_YEAR
from visualize import plot_altair_line_chart

st.markdown("<h1 style='text-align: center;'>Our World</h1>", unsafe_allow_html=True)


economy='WLD'
df_world=df_long[df_long['economy']==economy]
cols_to_keep=['Series','Year','Value']
df_world=df_world[cols_to_keep]

df_world=df_world.pivot(columns='Series',index='Year',values='Value')
chart_data=df_world.dropna(axis=1,how='all', ignore_index=False,inplace=False)
chart_data.reset_index(inplace=True)

tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Economy", "Market","Data"])

with tab2:
    base = alt.Chart(chart_data).encode(
        alt.X('Year:T').title('Year')
    ).properties(
        height=400,
        width=500
    )
    series='GDP (current US$)'
    # gdp = base.mark_line(stroke='#57A44C', point=True, interpolate='monotone').encode(
    #     alt.Y(series).title(series, titleColor='#57A44C'),
    #     tooltip=['Year:T',series]
    # )
    gdp = base.mark_bar(color='#5276A7',cornerRadius=2, width=12,binSpacing=0).encode(
        alt.Y(f'mean({series}):Q').title(series, color='#5276A7'),
        tooltip=['Year:T',series]
    )

    series='GDP growth (annual %)'
    gdp_growth = base.mark_line(stroke='#F18727', point=alt.OverlayMarkDef(color='#333'),
                                interpolate='monotone').encode(
        alt.Y(series).title(series, titleColor='#F18727').axis(titleColor='#F18727'),
        tooltip=['Year:T',series]
    )

    chart=alt.layer(gdp, gdp_growth).resolve_scale(
        y='independent'
    ).interactive()

    st.altair_chart(chart,use_container_width=True)

    with st.expander("See Data"):
        st.dataframe(chart_data)


with tab3:
    pass
