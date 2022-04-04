import plotly.graph_objects as go

def generatePieGraph(categories_total):
    """Generates a pie graph displaying the total spent per category."""

    # Stores keys and values from dict to use as labels and values in the charts.
    # Pie graph.
    pie_labels = categories_total.keys()
    pie_values = categories_total.values()

    # Casts into list for graph compatibility.
    # Pie graph.
    pie_labels = list(pie_labels)
    pie_values = list(pie_values)

    # Pie graph.
    Pie = go.Pie(labels=pie_labels, values=pie_values, hole=.3, 
        title_text="Categorias")
    pie_chart = go.Figure(data=Pie)
    pie_graph = pie_chart.to_html()

    return pie_graph

def generateBarGraph(x, y):
    """Generates a pie graph displaying the total spent per product."""

    Bar = go.Bar(x=x, y=y)
    layout = go.Layout(title="Productos y costo", xaxis={'title':'Productos'}, 
        yaxis={'title':'Costo'})
    figure = go.Figure(data=[Bar],layout=layout)
    bar_graph = figure.to_html()  

    return bar_graph  