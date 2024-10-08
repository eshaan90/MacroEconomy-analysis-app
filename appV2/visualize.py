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

def plot_altair_bar_chart():
    chart=None
    return chart
