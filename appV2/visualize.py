import altair as alt


def plot_altair_line_chart(df,x,y,xtype,ytype,xtitle,ytitle,title):
    chart=alt.Chart(df).mark_line(point=True).encode(
                x=alt.X(x,type=xtype,title=xtitle),
                y=alt.Y(y,type=ytype,title=None),#ytitle),
                # color='Country:N'
                ).properties(
                    # height=300,
                    # width=500,
                    title=title
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
    return chart

def plot_altair_multibar_chart(df,xtitle=None,ytitle=None,title='',subtitle=''):
    brush=alt.selection_interval(encodings=['x'],bind='scales')
    chart=alt.Chart(df,title=alt.Title(title,
                                                subtitle=subtitle)
                                                ).mark_bar().encode(
        x=alt.X('Year:O',timeUnit='year',title=xtitle),
        y=alt.Y('Value:Q',stack=None,title=ytitle),
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

    return chart
