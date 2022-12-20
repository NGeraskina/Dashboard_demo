import numpy as np
import pandas as pd
from dash import Dash, dcc, html, Input, Output

import plotly.graph_objects as go
import dash_bootstrap_components as dbc
import base64

# Компоненты дизайна

# цвета:
# '#3E5057' - темно синий
# '#8FC54C' - зеленый
#


background_color = 'white'
border_color = 'white'
font_color_dark = '#3E5057'
font_color_light = 'white'
font_color_green = '#8FC54C'
font_size_head = 25

### ------------------Данные--------------------------
df_fact = pd.DataFrame(
    {'date': ['01/01/2022', '02/01/2022', '03/01/2022', '04/01/2022', '05/01/2022'], 'plan': [370, 380, 390, 400, 410],
     'fact': [390, 395, 390, 393, 396]})
df_fact['ratio'] = df_fact.fact / df_fact.plan * 100

l_rand = [370] * 8
for i in range(1, len(l_rand)):
    l_rand[i] = l_rand[i - 1] + np.random.normal()

df_plan = pd.DataFrame(
    {'month': list(range(1, 9)), 'volume': l_rand})

# -------------Создание элементов дашборда-----------------------
head = dcc.Markdown('''**Наполнение счетов эскроу**, млрд руб''',
                    style={'font-family': 'Tahoma', 'font-size': font_size_head, 'color': font_color_dark,
                           'textAlign': 'center'})
card_2 = [
    dbc.CardHeader("План", style={'font-family': 'Tahoma', 'font-size': 20, "color": font_color_dark}),
    dbc.CardBody([html.B(
        1,
        id="card-text2", style={'font-family': 'Tahoma', 'font-size': 30, "color": font_color_green})])]

card_1 = [
    dbc.CardHeader("Факт", style={'font-family': 'Tahoma', 'font-size': 20, "color": font_color_dark}),
    dbc.CardBody(
        [html.B(
            2,
            id="card-text1", style={'font-family': 'Tahoma', 'font-size': 30, "color": font_color_green}), ]), ]

card_3 = [
    dbc.CardHeader("Факт/План %", style={'font-family': 'Tahoma', 'font-size': 20, "color": font_color_dark}),
    dbc.CardBody(
        [html.B(
            3,
            id="card-text3", style={'font-family': 'Tahoma', 'font-size': 30, "color": font_color_green}), ]), ]

row_1 = dbc.Row(
    [
        dbc.Col(dbc.Card(card_1, color=border_color, outline=True, className="text-center")),
        dbc.Col(dbc.Card(card_2, color=border_color, outline=True,
                         className="text-center")),

    ],
    className="mb-3"
    , style={'margin-top': '10px'}
)

row_2 = dbc.Row(dbc.Col(dbc.Card(card_3, color=border_color, outline=True,
                                 className="text-center")), className="mb-3")
image_filename = r'C:\Users\nadya\Downloads\noun-calendar-5386634.png'  # replace with your own image
encoded_image = base64.b64encode(open(image_filename, 'rb').read())
drop_down = dbc.Row(
    [html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()), style={'width': '60px', 'height': '40x'}),

     dcc.Dropdown(
         df_fact.date.unique(),
         df_fact.date.min(),
         id='date-fact',
         style={'font-family': 'Tahoma', 'font-size': 20, 'backgroundColor': background_color,
                'font-color': font_color_dark, "width": "70%", 'height': '40px'}), html.Br()
     #
     ])  #

graph = dcc.Graph(id='indicator-graphic', style={'backgroundColor': background_color}, config={
    'displayModeBar': False
})
slider = html.Div([html.Label("Плановый диапазон, кв.", htmlFor="month--slider"),
                   dcc.Slider(
                       df_plan.month.max() - 3,
                       df_plan.month.max(),
                       step=None,
                       id='month--slider',
                       value=5,
                       marks={str(month): {'label': str(month),
                                           'style': {'color': font_color_dark, 'font-family': 'Tahoma', 'size': 10}} for
                              month in df_plan.month.unique()[-4:]})], style={'margin-top': '15px'})

# ---------------------Создание приложения и выстраивание структуры дашборда из элементов---------------
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           meta_tags=[{'name': 'viewport',
                       'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5,'}]
           )
app.layout = html.Div([head, drop_down, row_1, row_2, graph, slider], style={'backgroundColor': background_color})


# -------------------------Функции обновления элементов дашборда-------------------------
@app.callback([Output('card-text1', 'children'), Output('card-text2', 'children'), Output('card-text3', 'children')],
              [Input('date-fact', 'value')])
def update_plan(date):
    dff = df_fact[df_fact.date == date]
    return f'{dff.fact.values[0]:0.0f}', f'{dff.plan.values[0]:0.0f}', f'{dff.ratio.values[0]:0.0f}',


@app.callback(
    Output('indicator-graphic', 'figure'),
    Input('month--slider', 'value'))
def update_graph(month_slider):
    dff = df_plan[df_plan['month'] <= month_slider]
    # fig = px.line(dff, x='month',
    #               y='volume',text="volume", markers=True, title="<b>План эскроу</b>"+", млрд руб")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dff.month, y=dff.volume, mode='lines+markers+text',
                             text=list(map(lambda x: f'{x:0.1f}', dff.volume.values)), textposition="top center",
                             textfont=dict(
                                 family="Tahoma",
                                 size=10,
                                 color="white"
                             )))
    fig.update_layout(title=dict(text="<b>План эскроу</b>" + ", млрд руб",
                                 font=dict(family='Tahoma', size=font_size_head, color=font_color_dark)),
                      font_family='Tahoma', font_size=10, plot_bgcolor='#3E5057', title_x=0.5,
                      yaxis_title=None,
                      xaxis_title='Кварталы', height=280, margin=dict(
            l=1,  # left
            r=5,  # right
            t=50,  # top
            b=5,  # bottom
        ))
    # fig.update_layout()
    fig.update_xaxes(showgrid=False)
    # fig.update_yaxes(title='y', )
    fig.update_yaxes(showgrid=False, gridwidth=0.1, gridcolor='grey', visible=True, showticklabels=False)
    fig.update_yaxes(range=[dff.volume.min() - 0.5, dff.volume.max() + 0.5])

    fig.update_traces(line_color='white')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)
