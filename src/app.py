import dash
from dash import html, State, Input, Output, callback
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import math

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])
server = app.server

border = {  'border': '1px outset black',  'border-radius': '5px'}
#########################
def getPrimes(limit):
    # The list of prime numbers
    primes = []
    # The boolean list of whether a number is prime
    numbers = [True] * limit
    # Loop all of the numbers in numbers starting from 2
    for i in range(2, limit):
        # If the number is prime
        if numbers[i]:
            # Add it onto the list of prime numbers
            primes.append(i)
            # Loop over all of the other factors in the list
            for n in range(i ** 2, limit, i):
                # Make them not prime
                numbers[n] = False

    # Return the list of prime numbers
    return primes
offcanvas = html.Div(
    [
        dbc.Button(' Calculation returns Material R.P.M. & Feedrate ', id="open-offcanvas", n_clicks=0),
        dbc.Offcanvas(
            
            html.P([
                " Input: ",html.Br(),
                "   * wheel diameter",html.Br(),
                "   * wheel width",html.Br(),
                "   * wheel RPM ",html.Br(),
                "   * material diameter",html.Br(),
                html.Br(),

                " Output: ",html.Br(),
                "   * material RPM (prime number)",html.Br(),
                "   * RPM ratio (strange number)",html.Br(),
                "   * feedrate",html.Br(),
                "   * speed ratio (for ref. only)", html.Br(),
                "   * overlap (for ref. only) ",html.Br(),
    ]),
            id="offcanvas",
            title="How to use ?",
            is_open=False,
            placement='end',
        ),
    ]
)


app.layout = html.Div([
    # html.H5(' Calculation returns Material R.P.M. & Feedrate '),
    offcanvas,
    dbc.Row([
    dbc.Col([
                dbc.InputGroup([dbc.InputGroupText("Wheel ø [mm]"), dbc.Input(id='wheel_d_2',type='number', value=350)]),
                dbc.InputGroup([dbc.InputGroupText("Wheel width [mm]"), dbc.Input(id='wheel_width_2',type='number', value=5)]),
                dbc.InputGroup([dbc.InputGroupText("Wheel R.P.M"), dbc.Input(id='wheel_rpm_2',type='number', value=5200)]),
                html.Br(),
                dbc.InputGroup([dbc.InputGroupText("Material ø "), dbc.Input(id='material_d_2',type='number', value=10, step= 0.1), ]),
                #dbc.InputGroup([dbc.InputGroupText("Depth of cut"), dbc.Input(id='depth_of_cut_2',type='number', value=0.025)]),
                html.Br(),
              
                dbc.InputGroup([dbc.InputGroupText("Speed ratio [qs] *"), dbc.Input(id='speed_ratio_2',type='number', value= 276.92 )]),
                dbc.InputGroup([dbc.InputGroupText("Overlap [Ud] *  "), dbc.Input(id='overlap_2',type='number', value = 73.07 )]),
                
                html.H6(' * - values used to calculate Material R.P.M. & Feedrate, '), 
                html.Br(),
                ]
                ,className="mb-3", width=3, style=border),
    dbc.Col([
                html.Br(),
                dbc.InputGroup([dbc.InputGroupText("Material R.P.M"), dbc.InputGroupText(id='material_rpm_2'),]),
                dbc.InputGroup([dbc.InputGroupText("RPM ratio [revs/revs] *"), dbc.InputGroupText(id='rpm_ratio_2'),]),
                dbc.InputGroup([dbc.InputGroupText("Feedrate [mm/min]"), dbc.InputGroupText(id='traverse_feedrate_2'),]),
                # dbc.InputGroup([dbc.InputGroupText("RPM ratio [revs/rev]"), dbc.InputGroupText(id='overlap_ratio'),]),

       
    ],className="mb-3", width=3, style = border),

])
])
@callback(
    Output("material_rpm_2", "children"),
    Output("traverse_feedrate_2", "children"),
    Output('speed_ratio_2', 'value'),
    Output('overlap_2' , 'value'),
    Output('rpm_ratio_2', 'children'),
    Input("wheel_d_2", "value"),
    Input("wheel_rpm_2", "value"),
    Input("wheel_width_2", "value"),
    Input("material_d_2", "value"),

    )

def feed_rate_calculation(wheel_d, wheel_rpm, wheel_width, material_d, ): 
    ''' Function calculates basic parameters for OD grinding process (traverse grinding)
        Purpose is to find correct value of Speed Ratio & UD 
        which are used to calculate material speed  and traverse feedrate.
        Speed ratio range: 200 ~ 300
        Overlap ration range: 50 ~80
         
    '''
    
    # if wheel_d or wheel_rpm or  wheel_width or  material_d  is None:
    #     raise PreventUpdate    

    speed_min, speed_max  = 200, 300 
    overlap_min, overlap_max  = 50, 80
    dia_min, dia_max =  4 , 30

    # Sugerowane współczynniki : prędkości / nakładania

    speed_ratio = speed_max - ( material_d - dia_min) * ( speed_max - speed_min ) / (dia_max - dia_min)
    overlap_ratio = overlap_max - ( material_d - dia_min) * ( overlap_max - overlap_min ) / (dia_max - dia_min)


    wheel_speed = (wheel_d * math.pi * wheel_rpm) / (60 * 1000)
    material_speed = wheel_speed / speed_ratio
    
    # Sprawdzenie czy wartość obrotów narzędzia jest liczbą piewrszą
    # material_rpm = round((material_speed * 60 * 1000) / (material_d * math.pi), 0)
    number = int((material_speed * 60 * 1000) / (material_d * math.pi))
    print(number)
    primes = getPrimes(number + 100)
    maxDist = 99999999
    umb = 0
    for p in primes:
    # If the prime number is closer than maxDist
        if abs(number - p) < maxDist:
            # Set maxDist to the number
            maxDist = abs(number - p)
            # Set numb to the number
            material_rpm = p




    #q_prime = (depth_of_cut * material_rpm * material_d * math.pi) / 60 
    feed_rate = round((material_rpm * wheel_width) / overlap_ratio , 0)

    speed_ratio = speed_max - ( material_d - dia_min) * ( speed_max - speed_min ) / (dia_max - dia_min)
    overlap_ratio = overlap_max - ( material_d - dia_min) * ( overlap_max - overlap_min ) / (dia_max - dia_min)
    # print((np.floor(speed_ratio)))
    # print((np.floor(overlap_ratio)))

    rpm_ratio = wheel_rpm/material_rpm


    return material_rpm, feed_rate, speed_ratio, overlap_ratio, rpm_ratio

@callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open

# wskazniki = ['Heating','HotWater','ProducedHeating','ProducedHotWater']



# # df_read = pd.read_excel('https://github.com/McKenzi84/EyesOnTheWorld/blob/main/energia.xlsx')
# df_read = pd.read_csv('https://raw.githubusercontent.com/McKenzi84/EyesOnTheWorld/main/energia.csv')
# df_read['year'] = pd.DatetimeIndex(df_read['Date']).year
# df_read['month'] = pd.DatetimeIndex(df_read['Date']).month
# df_read['day'] =pd.DatetimeIndex(df_read['Date']).day


# df_read['PC_pobór'] = df_read['Heating'] + df_read['HotWater']
# df_read['PC_produkcja'] = df_read['ProducedHeating'] + df_read['ProducedHotWater']

# df = df_read[['year','month','day', 'pv', 'TA-pobór','TA-generacja', 'PC_pobór', 'PC_produkcja']]

# print(df['year'].unique())


# metrics = df.columns[3:7]
# #metrics = ['pv']

# app.layout = dbc.Container([
#                 dbc.Row([
#                         dbc.Col([
#                             #dcc.Location(id='url', refresh=False),  #this locates this structure to the url
#                             #dcc.Store(id='store-data', data=[], storage_type='memory'), # 'local' or 'session'
#                             dcc.Dropdown(id='year_selection',options= [{'label': x, 'value': x} for x in df['year'].unique()], multi=True, value=[2022],clearable=False),
#                             dcc.Dropdown(id='metric_selection',options= [{'label': x, 'value': x} for x in metrics], multi=True, value=['pv']),
                            
#                             dcc.Graph(id='graph2'),
#                             dcc.RangeSlider(id='month_range',min=1, max=12, value=[1,12], step= 1, allowCross=False,
#                             marks={
#                                     1: {'label': 'Sty'},
#                                     2: {'label': 'Lut'},
#                                     3: {'label': 'Mar'},
#                                     4: {'label': 'Kwi'},
#                                     5: {'label': 'Maj'},
#                                     6: {'label': 'Cze'},
#                                     7: {'label': 'Lip'},
#                                     8: {'label': 'Sie'},
#                                     9: {'label': 'Wrz'},
#                                     10: {'label': 'Paź'},
#                                     11: {'label': 'Lis'},
#                                     12: {'label': 'Gru'}
#                                 })
                            

#                         ], xs=12, sm=12, md=12, lg=12 , xl=12), # End of Col
#                         dbc.Col([
#                             html.Br(),
#                             html.Br(),
#                             html.Br(),
#                             html.Br(),
#                             html.Br(),
#                             html.P('Podsumowanie dla wybranego okresu'),
#                             html.Div(id='table'),

#                         ], xs=12, sm=12, md=12, lg=4 , xl=4) # End of Col 2


#                 ],style = {  'border': '5px outset black',  'border-radius': '10px'})# End of Row



# ], className="pt-4", fluid=True,)# End of container

    
# ##wykres 
# @app.callback(Output('graph2', 'figure'),
#                # Output('table', 'children'),
#                #Output('slider', 'children'),
#                 Input('year_selection','value'),
#                 Input('month_range', 'value'),
#                 Input('metric_selection', 'value'),
                
#                 )

# def bar_graph2(selected_year, selected_month, selected_metric):
#     #print(selected_year)
#     figure = go.Figure()


#     #figure.add_trace(go.Scatter(x=dff['month'], y=dff['Consumed_total'], line_shape='hv'))
    
#     # Dodanie do wykresu ( Melcloud )
#     for r in sorted(selected_year):
#         for w in selected_metric:
#             dff = df.loc[(df['year']==r)&(df['month'].isin(range(selected_month[0],selected_month[1]+1)))].groupby(['month']).agg({w:'sum'}).round(0).reset_index()
#             figure.add_trace(go.Bar(x=dff['month'], y=dff[w], name=f'{r}/{w}/',text=dff[w],))
#             #print(dff)


#     opis = f'''
    
#     '''
#     legend=dict(
#     # yanchor="top",
#     # y=0.99,
#     # xanchor="left",
#     # x=0.15,
#     font = dict(family = "Courier", size = 20  , color = "white"),

#     )

#     layout = go.Layout(title=opis,
#                         font_color= 'white' , paper_bgcolor = 'rgba(0,0,0,0)',plot_bgcolor = 'rgba(0,0,0,0)', height=600,
#                         xaxis = dict(tickmode = 'array',tickvals = [1,2,3,4,5,6,7,8,9,10,11,12], 
#                                                         ticktext = ['Sty','Lut','Mar','Kwi','Maj','Cze','Lip','Sie','Wrz','Paź','Lis','Gru' ]),legend = legend )

#     #figure.update_traces(hoverinfo='text+name', mode='lines+markers')
#     figure.update_layout(layout)
#     figure.update_yaxes(title_text = 'kWh', title_standoff = 25)
#     figure.update_traces(textfont_size=15,  textangle=-1, textposition="outside")

    
    
#     return figure

# #Table
# @app.callback( Output('table', 'children'),
#                #Output('slider', 'children'),
#                 Input('year_selection','value'),
#                 Input('month_range', 'value'),
#                 Input('metric_selection', 'value'),
                
#                 )

# def table_update(selected_year, selected_month, selected_metric):
#     #print(type(selected_year))
#     metrics_agg = {x : 'sum' for x in selected_metric}
#     #dff_table = df.loc[(df['year'].isin(selected_year))&df['month'].isin(range(selected_month[0],selected_month[1]+1))].groupby(['year']).agg({selected_metric[0]:'sum'}).round(0).reset_index()
#     dff_table = df.loc[(df['year'].isin(selected_year))& (df['month'].isin(range(selected_month[0],selected_month[1]+1)))].groupby(['year']).agg(metrics_agg).round(0).reset_index()

#     for x in selected_metric:
#         print(x)
    
   
#     # print(selected_year)
#     #print(dff_table)
#     table = dash_table.DataTable(
#     # id='table',
#     columns=[{"name": i, "id": i} for i in dff_table.columns],
#     data=dff_table.to_dict('records'),
#     )

#     return table
    


if __name__ == "__main__":
    # app.run_server(debug=True, host = '0.0.0.0' ,port=1112)
    app.run_server(debug=True,)