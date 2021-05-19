import plotly.figure_factory as ff
from plotly.offline import plot


def get_graph_html():
    df = [dict(Task="Task 1", Start='2021-02-02', Finish='2021-03-29'),
          dict(Task="Task 2", Start='2021-04-06', Finish='2021-05-24'),
          dict(Task="Task 3", Start='2021-03-30', Finish='2021-06-29')]

    fig = ff.create_gantt(df)
    plot_fig = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_fig
