import pandas as pd

from chickflow.charts import ALERT, TEAL, stock_chart


def test_stock_chart_colors_follow_reorder_status():
    stock = pd.DataFrame({
        "ingredient_name": ["Saus teriyaki", "Selada"],
        "city": ["Payakumbuh", "Padang"],
        "stock_qty": [48, 148],
        "reorder_point_qty": [103, 100],
        "reorder_ratio": [48 / 103, 1.48],
        "unit": ["ml", "g"],
        "critical": [True, False],
    })
    chart = stock_chart(stock)
    assert {trace.name: trace.marker.color for trace in chart.data} == {
        "Di bawah batas": ALERT, "Mencapai batas": TEAL,
    }
    assert chart.layout.shapes[0].x0 == chart.layout.shapes[0].x1 == 1
    assert list(chart.data[0].customdata[0]) == [48, 103, "ml"]
