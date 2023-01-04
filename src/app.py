import dash
from dash import html, dcc, Input, Output, dash_table
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objs as go

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])
server = app.server

wskazniki = ['Heating','HotWater','ProducedHeating','ProducedHotWater']



# df_read = pd.read_excel('https://github.com/McKenzi84/EyesOnTheWorld/blob/main/energia.xlsx')
df_read = pd.read_csv('https://github.com/McKenzi84/EyesOnTheWorld/blob/main/energia.csv')
df_read['year'] = pd.DatetimeIndex(df_read['Date']).year
df_read['month'] = pd.DatetimeIndex(df_read['Date']).month
df_read['day'] =pd.DatetimeIndex(df_read['Date']).day


df_read['PC_pobór'] = df_read['Heating'] + df_read['HotWater']
df_read['PC_produkcja'] = df_read['ProducedHeating'] + df_read['ProducedHotWater']

df = df_read[['year','month','day', 'pv', 'TA-pobór','TA-generacja', 'PC_pobór', 'PC_produkcja']]

print(df['year'].unique())


metrics = df.columns[3:7]
#metrics = ['pv']

app.layout = dbc.Container([
                dbc.Row([
                        dbc.Col([
                            #dcc.Location(id='url', refresh=False),  #this locates this structure to the url
                            #dcc.Store(id='store-data', data=[], storage_type='memory'), # 'local' or 'session'
                            dcc.Dropdown(id='year_selection',options= [{'label': x, 'value': x} for x in df['year'].unique()], multi=True, value=[2022],clearable=False),
                            dcc.Dropdown(id='metric_selection',options= [{'label': x, 'value': x} for x in metrics], multi=True, value=['pv']),
                            
                            dcc.Graph(id='graph2'),
                            dcc.RangeSlider(id='month_range',min=1, max=12, value=[1,12], step= 1, allowCross=False,
                            marks={
                                    1: {'label': 'Sty'},
                                    2: {'label': 'Lut'},
                                    3: {'label': 'Mar'},
                                    4: {'label': 'Kwi'},
                                    5: {'label': 'Maj'},
                                    6: {'label': 'Cze'},
                                    7: {'label': 'Lip'},
                                    8: {'label': 'Sie'},
                                    9: {'label': 'Wrz'},
                                    10: {'label': 'Paź'},
                                    11: {'label': 'Lis'},
                                    12: {'label': 'Gru'}
                                })
                            

                        ], xs=12, sm=12, md=12, lg=12 , xl=12), # End of Col
                        dbc.Col([
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.Br(),
                            html.P('Podsumowanie dla wybranego okresu'),
                            html.Div(id='table'),

                        ], xs=12, sm=12, md=12, lg=4 , xl=4) # End of Col 2


                ],style = {  'border': '5px outset black',  'border-radius': '10px'})# End of Row



], className="pt-4", fluid=True,)# End of container

    
##wykres 
@app.callback(Output('graph2', 'figure'),
               # Output('table', 'children'),
               #Output('slider', 'children'),
                Input('year_selection','value'),
                Input('month_range', 'value'),
                Input('metric_selection', 'value'),
                
                )

def bar_graph2(selected_year, selected_month, selected_metric):
    #print(selected_year)
    figure = go.Figure()


    #figure.add_trace(go.Scatter(x=dff['month'], y=dff['Consumed_total'], line_shape='hv'))
    
    # Dodanie do wykresu ( Melcloud )
    for r in sorted(selected_year):
        for w in selected_metric:
            dff = df.loc[(df['year']==r)&(df['month'].isin(range(selected_month[0],selected_month[1]+1)))].groupby(['month']).agg({w:'sum'}).round(0).reset_index()
            figure.add_trace(go.Bar(x=dff['month'], y=dff[w], name=f'{r}/{w}/',text=dff[w],))
            #print(dff)


    opis = f'''
    
    '''
    legend=dict(
    # yanchor="top",
    # y=0.99,
    # xanchor="left",
    # x=0.15,
    font = dict(family = "Courier", size = 20  , color = "white"),

    )

    layout = go.Layout(title=opis,
                        font_color= 'white' , paper_bgcolor = 'rgba(0,0,0,0)',plot_bgcolor = 'rgba(0,0,0,0)', height=600,
                        xaxis = dict(tickmode = 'array',tickvals = [1,2,3,4,5,6,7,8,9,10,11,12], 
                                                        ticktext = ['Sty','Lut','Mar','Kwi','Maj','Cze','Lip','Sie','Wrz','Paź','Lis','Gru' ]),legend = legend )

    #figure.update_traces(hoverinfo='text+name', mode='lines+markers')
    figure.update_layout(layout)
    figure.update_yaxes(title_text = 'kWh', title_standoff = 25)
    figure.update_traces(textfont_size=15,  textangle=-1, textposition="outside")

    
    
    return figure

#Table
@app.callback( Output('table', 'children'),
               #Output('slider', 'children'),
                Input('year_selection','value'),
                Input('month_range', 'value'),
                Input('metric_selection', 'value'),
                
                )

def table_update(selected_year, selected_month, selected_metric):
    #print(type(selected_year))
    metrics_agg = {x : 'sum' for x in selected_metric}
    #dff_table = df.loc[(df['year'].isin(selected_year))&df['month'].isin(range(selected_month[0],selected_month[1]+1))].groupby(['year']).agg({selected_metric[0]:'sum'}).round(0).reset_index()
    dff_table = df.loc[(df['year'].isin(selected_year))& (df['month'].isin(range(selected_month[0],selected_month[1]+1)))].groupby(['year']).agg(metrics_agg).round(0).reset_index()

    for x in selected_metric:
        print(x)
    
   
    # print(selected_year)
    #print(dff_table)
    table = dash_table.DataTable(
    # id='table',
    columns=[{"name": i, "id": i} for i in dff_table.columns],
    data=dff_table.to_dict('records'),
    )

    return table
    


if __name__ == "__main__":
    # app.run_server(debug=True, host = '0.0.0.0' ,port=1112)
    app.run_server(debug=True,)