import altair as alt
import pandas as pd

def plot_altair_line_chart(df,x,y,xtype,ytype,events_df=pd.DataFrame(),xtitle='',ytitle='',title=''):
    '''
    '''
    brush = alt.selection_interval(encodings=['x'])
    # selection = alt.selection_interval(bind='scales')
    line=alt.Chart(df).mark_line(point=alt.OverlayMarkDef(color='#333'),color="#333").encode(
                x=alt.X(x,type=xtype,title=xtitle),#.scale(domain=brush),
                y=alt.Y(y,type=ytype,title=None),#ytitle),
                color=alt.condition(brush, alt.Color('Country:N').legend(orient='bottom'), alt.value('lightgray'))
                # color='Country:N'
                ).properties(
                    # height=300,
                    # width=500,
                    title=title
                ).add_params(
                    brush,
                    # selection
                )
    # point = line.mark_point(color="#333")

    # .configure_title(
    #         fontSize=20,
    #         font='Courier',
    #         anchor='start',
    #         color='gray'
    #     )

    if not events_df.empty:
        color_scale = alt.Scale(range=['#1f77b4', '#e377c2'])
        rect = alt.Chart(events_df).mark_rect().encode(
                x="start:T",
                x2="end:T",
                color=alt.Color("event:N",title="Event").scale(color_scale).legend(orient='bottom'),
                opacity=alt.value(0.2)
            )
        return rect+line

    return line

def plot_altair_bar_chart(df,x,y,xtype,ytype,xtitle=None,ytitle=None,title='',subtitle=''):
    '''
    '''
    brush=alt.selection_interval(encodings=['x'],bind='scales')
    chart=alt.Chart(df,title=alt.Title(title,
                                                subtitle=subtitle)
                                                ).mark_bar().encode(
        x=alt.X(x,type=xtype,timeUnit='year',title=xtitle),
        y=alt.Y(y,type=ytype,stack=None,title=ytitle),
        # tooltip=['Year:T','Country:N','Value:Q']
    ).properties(
        # height=500,
        # width=300
    ).add_params(
                # selection,
                brush
    )#.interactive()

    chart.configure_title(
            fontSize=20,
            font='Courier',
            anchor='start',
            color='gray'
        )
    return chart

def plot_altair_bar_chart_with_mean(df,x,y,xtype,ytype,events_df=pd.DataFrame(),xtitle=None,ytitle=None,title='',subtitle=''):
    brush = alt.selection_interval(encodings=['x'])

    bars = alt.Chart(df).mark_bar().encode(
        x=alt.X(x,type=xtype,title=xtitle),
        xOffset="Country:N",
        y=alt.Y(y,type=ytype,stack=None,title=ytitle),
        color=alt.condition(brush, alt.Color('Country:N').legend(orient='bottom'), alt.value('lightgray')),
        opacity=alt.condition(brush, alt.OpacityValue(1), alt.OpacityValue(0.7)),
        tooltip=[x,y,'Country:N']
    ).add_params(
        brush
    )


    if df['Country'].nunique()>1:
        # return bars
        if not events_df.empty:
            color_scale = alt.Scale(range=['#1f77b4', '#e377c2'])
            rect = alt.Chart(events_df).mark_rect().encode(
                    x="start:T",
                    x2="end:T",
                    color=alt.Color("event:N",title="Event").scale(color_scale).legend(orient='bottom'),
                    opacity=alt.value(0.2)
                )
            return bars+rect
        return bars
    else:
        line = alt.Chart().mark_rule(color='firebrick').encode(
            y=alt.Y(y,aggregate='mean',type=ytype),
            size=alt.SizeValue(3)
        ).transform_filter(
            brush
        )
        if not events_df.empty:
            color_scale = alt.Scale(range=['#1f77b4', '#e377c2'])
            rect = alt.Chart(events_df).mark_rect().encode(
                    x="start:N",
                    x2="end:N",
                    color=alt.Color("event:N",title="Event").scale(color_scale).legend(orient='bottom'),
                    opacity=alt.value(0.2)
                )
            return bars+rect

        return  alt.layer(bars, line,data=df)

def plot_altair_multibar_chart(df,x,y,xtype,ytype,xtitle=None,ytitle=None,title='',subtitle=''):
    brush=alt.selection_interval(encodings=['x'],bind='scales')
    chart=alt.Chart(df,title=alt.Title(title,
                                                subtitle=subtitle)
                                                ).mark_bar().encode(
        x=alt.X(x,type=xtype,timeUnit='year',title=xtitle),
        y=alt.Y(y,type=ytype,stack=None,title=ytitle),
        # xOffset="Country:N",
        # color=alt.Color('Country:N').legend(orient='bottom'),
        # column=alt.Column('Country:N',align='each',center=True),
        
        # tooltip=['Year:T','Country:N','Value:Q']
    ).properties(
        # height=500,
        # width=300
    ).add_params(
                # selection,
                brush
    )#.interactive()

    chart.configure_title(
            fontSize=20,
            font='Courier',
            anchor='start',
            color='gray'
        )
    return chart
