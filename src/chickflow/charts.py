from collections import defaultdict

import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from chickflow.metrics import WEEKDAYS

BRICK, BLUE, TEAL, ALERT = "#963C32", "#376982", "#35695E", "#9E332D"
PANEL, TEXT, MUTED, GRID = "#FFFFFF", "#262624", "#53534D", "#E7E6E1"
CATEGORY_COLORS = dict(zip(
    ("Fried Chicken","Burger","Rice Meal","Wings","Sides","Beverage","Combo"),
    (TEAL,BLUE,"#556982","#75588A","#79734B","#30717D",BRICK),
))


def layout(figure, x="", y="", height=340):
    return figure.update_layout(
        template="plotly_white", paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        font=dict(color=TEXT, family="Avenir Next, system-ui, sans-serif", size=12),
        xaxis_title=x, yaxis_title=y, height=height,
        margin=dict(l=22,r=24,t=16,b=44), legend_title_text="",
        legend=dict(orientation="h", y=1.08),
        hoverlabel=dict(bgcolor=PANEL, font_color=TEXT, bordercolor=MUTED),
    ).update_xaxes(gridcolor=GRID,automargin=True).update_yaxes(gridcolor=GRID,automargin=True)


def revenue_line(table, height=290):
    fig = go.Figure(go.Scatter(x=table.date,y=table.revenue,mode="lines+markers",
                               line=dict(color=BRICK,width=2.5),marker=dict(size=5),
                               fill="tozeroy", fillcolor="#F1EAE5",
                               hovertemplate="%{x|%d/%m}<br>Rp%{y:,.0f}<extra></extra>"))
    return (layout(fig,"Tanggal WIB","Rupiah",height)
            .update_xaxes(tickformat="%d/%m")
            .update_yaxes(tickprefix="Rp",rangemode="tozero"))


def horizontal_bar(table, x, y, label, color=BLUE, currency=False):
    fig = px.bar(table.sort_values(x),x=x,y=y,orientation="h",color_discrete_sequence=[color],
                 labels={x:label,y:""},hover_data={x:":,.0f" if currency else True})
    return layout(fig,label,"",max(190,min(390,110+25*len(table)))).update_xaxes(
        tickprefix="Rp" if currency else "",zeroline=True,rangemode="tozero"
    )


def order_heatmap(cells):
    grid = cells.set_index(["day","hour"]).reindex([(d,h) for d in WEEKDAYS for h in range(10,22)])
    custom = np.stack((grid.orders.to_numpy().reshape(7,12),grid.days.to_numpy().reshape(7,12)),axis=-1)
    fig = go.Figure(go.Heatmap(x=list(range(10,22)),y=WEEKDAYS,z=grid.daily_mean.to_numpy().reshape(7,12),
                              colorbar_title="Pesanan/hari",zmin=0,customdata=custom,hoverongaps=False,
                              colorscale=[[0,"#F1EAE6"],[.55,"#B77E6F"],[1,"#8C493C"]],
                              hovertemplate="%{y} · %{x}:00<br>%{z:.1f} pesanan/hari<br>Total %{customdata[0]} dari %{customdata[1]} hari<extra></extra>"))
    return layout(fig,"Jam WIB","",285).update_yaxes(autorange="reversed").update_xaxes(dtick=2)


def prep_histogram(orders):
    fig = px.histogram(orders,x="prep_time_min",color_discrete_sequence=[BLUE])
    fig.update_traces(xbins=dict(size=2),autobinx=False)
    fig.add_vline(x=float(orders.prep_time_min.median()),line_color=BRICK,line_dash="dash",
                  annotation_text="Median",annotation_position="top right")
    return layout(fig,"Menit","Pesanan",290)


def prep_box(orders):
    fig = px.box(orders,x="prep_time_min",y="city",points="outliers",color_discrete_sequence=[BLUE],
                 labels={"city":"Cabang","prep_time_min":"Menit"})
    return layout(fig,"Menit","Cabang",280).update_xaxes(rangemode="tozero")


def delay_bars(table):
    colors = {"Bawa pulang":TEAL,"Pesan antar":BLUE,"Makan di tempat":"#936824"}
    fig = px.bar(table,x="rate",y="city",color="channel_name",barmode="group",orientation="h",
                 color_discrete_map=colors,custom_data=["late","n"],labels={"rate":"Terlambat"})
    fig.update_traces(hovertemplate="%{y}<br>%{x:.1%} (%{customdata[0]}/%{customdata[1]})")
    return layout(fig,"Terlambat","Cabang",290).update_xaxes(tickformat=".0%",rangemode="tozero")


def stock_chart(stock):
    shown = stock.assign(
        label=stock.ingredient_name + " · " + stock.city,
        status=stock.critical.map({True:"Di bawah batas",False:"Mencapai batas"}),
    ).sort_values("reorder_ratio")
    fig = px.bar(shown, x="reorder_ratio", y="label", orientation="h", color="status",
                 category_orders={"label":shown.label.tolist()},
                 color_discrete_map={"Di bawah batas":ALERT,"Mencapai batas":TEAL},
                 custom_data=["stock_qty","reorder_point_qty","unit"])
    fig.update_traces(
        hovertemplate="%{y}<br>Saldo %{customdata[0]} %{customdata[2]}"
                      "<br>Batas %{customdata[1]} %{customdata[2]}<br>Rasio %{x:.1%}<extra></extra>"
    )
    fig.add_vline(x=1,line_color=MUTED,line_dash="dash")
    return (layout(fig,"Saldo ÷ batas pesan ulang","",max(220,120+25*len(shown)))
            .update_xaxes(tickformat=".0%",rangemode="tozero")
            .update_layout(legend=dict(y=1.025,yanchor="bottom"),margin=dict(t=44)))


def stock_history(dates, balances, reorder, unit):
    fig = go.Figure(go.Scatter(x=dates,y=balances,mode="lines+markers",
                                line=dict(color=TEAL,width=2.5),name="Saldo akhir"))
    fig.add_hline(y=reorder,line_color=BRICK,line_dash="dash",annotation_text="Batas pesan ulang")
    return (layout(fig,"Tanggal WIB",unit,290).update_xaxes(tickformat="%d/%m")
            .update_yaxes(rangemode="tozero"))


def margin_scatter(menu, threshold=.25):
    fig = px.scatter(menu,x="units",y="margin",color="category",color_discrete_map=CATEGORY_COLORS,
                     hover_name="menu_name",hover_data={"revenue":":,.0f","cogs":":,.0f","profit":":,.0f","margin":":.1%"},
                     labels={"units":"Unit menu","margin":"Margin","revenue":"Omzet",
                             "cogs":"Biaya bahan dan kemasan","profit":"Laba kotor makanan"})
    fig.update_traces(marker=dict(size=12,line=dict(width=1,color=PANEL)))
    fig.add_hline(y=threshold,line_color=MUTED,line_dash="dash")
    return layout(fig,"Unit terjual","Margin kotor makanan",330).update_yaxes(tickformat=".0%")


def city_map(table, online=False, boundary=None):
    fig = go.Figure()
    if not online and boundary:
        geometry = boundary["geometry"]
        polygons = geometry["coordinates"] if geometry["type"] == "MultiPolygon" else [geometry["coordinates"]]
        edges = defaultdict(list)
        for rings in polygons:
            longitude, latitude = zip(*rings[0])
            edges["lon"].extend([*longitude, None])
            edges["lat"].extend([*latitude, None])
        fig.add_trace(go.Scatter(x=edges["lon"],y=edges["lat"],mode="lines",fill="toself",
                                 fillcolor="#C6D7C9",line=dict(color="#728C7D",width=1),
                                 hoverinfo="skip",showlegend=False))
    positions = {"Padang":"bottom center","Bukittinggi":"top left","Payakumbuh":"top right"}
    largest_sales = max(int(table.revenue.max()), 1)
    for city in table.itertuples():
        size = max(8, 33*np.sqrt(city.revenue / largest_sales))
        marks = dict(text=[city.city],name=city.city,marker=dict(size=size,color=BRICK,opacity=.9),
                     mode="markers+text",textposition=positions.get(city.city,"top center"),
                     textfont=dict(color=TEXT),showlegend=False,customdata=[[city.revenue,city.orders]],
                     hovertemplate="%{text}<br>Omzet Rp%{customdata[0]:,.0f}<br>%{customdata[1]} pesanan<extra></extra>")
        if online:
            fig.add_trace(go.Scattermap(lat=[city.latitude],lon=[city.longitude],**marks))
        else:
            fig.add_trace(go.Scatter(x=[city.longitude],y=[city.latitude],**marks))
    fig = layout(fig,height=292).update_layout(margin=dict(l=0,r=0,t=0,b=0))
    if online:
        return fig.update_layout(map=dict(center={"lat":-.59,"lon":100.47},zoom=7.1,style="carto-positron"))
    # These city coordinates are near the equator, so equal scales are appropriate for this local view.
    return (fig.update_layout(plot_bgcolor="#E5EEE8",dragmode="pan")
            .update_xaxes(range=[99.57,101.38],visible=False)
            .update_yaxes(range=[-1.2,-.06],visible=False,scaleanchor="x",scaleratio=1))
