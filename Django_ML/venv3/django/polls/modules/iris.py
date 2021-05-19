import plotly.express as px
from plotly.offline import plot
from sklearn import linear_model as sk_lr
from sklearn.metrics import mean_squared_error, r2_score


def get_graph_html():
    fig = px.scatter(px.data.iris(), x='sepal_length', y='petal_length', color='species', symbol='species'
                     , trendline='ols',
                     hover_data=['species_id'], width=400, height=300, title='sepal_length & petal_length')
    fig.update_xaxes(title_text='sepal_length', range=[4, 8], row=1, col=1)
    fig.update_yaxes(title_text='petal_length', range=[0.5, 8], row=1, col=1)
    plot_fig = plot(fig, output_type='div', include_plotlyjs=False)

    return plot_fig


def get_graph_html_virginica(input):
    df_virginica = px.data.iris().loc[
        px.data.iris()['species'] == 'virginica', ['sepal_length', 'petal_length', 'species']]

    X = df_virginica.loc[:, ['sepal_length']].values
    y = df_virginica.loc[:, ['petal_length']].values

    lr = sk_lr.LinearRegression()
    lr.fit(X, y)
    y_pred = lr.predict(X)
    params = [lr.coef_[0][0], mean_squared_error(y, y_pred), r2_score(y, y_pred)]
    params = [round(x, 2) for x in params]

    prediction = None
    if (input != None):
        pred = lr.predict([[input]])
        prediction = pred[0][0]
        new_row = {'sepal_length': input, 'petal_length': prediction, 'species': 'prediction'}
        df_virginica = df_virginica.append(new_row, ignore_index=True)

    fig = px.scatter(df_virginica, x='sepal_length', y='petal_length', color='species', symbol='species'
                     , trendline='ols',
                     hover_data=['species'], width=400, height=300, title='sepal_length & petal_length')
    fig.update_xaxes(title_text='sepal_length', range=[4.5, 8], row=1, col=1)
    fig.update_yaxes(title_text='petal_length', range=[3, 8], row=1, col=1)

    # fig.show()   #for debug
    # print(df_virginica) #for debug

    plot_fig = plot(fig, output_type='div', include_plotlyjs=False)
    return {'plot_fig': plot_fig, 'params': params, 'prediction': prediction if prediction else "No result"}

# get_graph_html_virginica(5) # for debug
