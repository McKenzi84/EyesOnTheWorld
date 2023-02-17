import dash 
import dash_bootstrap_components as dbc
from dash import html, dcc, callback , Input , Output, State
from dash.exceptions import PreventUpdate
#import ezdxf
import plotly.graph_objects as go

from drawing import Drawing


app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])
server = app.server

border = {  'border': '1px outset black',  'border-radius': '5px'}

# Zawartość drop-dałnów

steps = [1,2,3,]


column1 = [ html.Br(),
            html.H6('1. Tool info'),
            dcc.Dropdown(id='s_steps',options=[{'label': f'  No of diameters: {x}', 'value': (x)} for x in steps],style={'color':'black', 'width': '100%'},placeholder="How many diameters", value=1),
            
            dbc.InputGroup([
                    dbc.InputGroupText('Point angle °'), 
                    dbc.Input(id= 'point_angle',type='number', value=135, min=60, max=180),
                    #dbc.InputGroupText('Helix °'),  
                    #dbc.Input(id= 'helix_angle',type='number', value=30),],
                    ],size='sm'),                                              
            
            
            html.Div(id='d1_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 1'),
                                                dbc.Input(id='d1',type='number',min=3, max=35,  value=10), 
                                                dbc.InputGroupText('ø 1 length'),
                                                dbc.Input(id='d1_l',type='number', value= 40, min=20, max=150),
                                                # dbc.Checkbox(id="standalone-checkbox",value=True,)
                                                ],size='sm',), style={'display':'block'}),
            html.Div(id='d1_details_multi',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 1'),
                                                dbc.Input(id='d1_multi',type='number',min=3, max=35,  value=10), 
                                                dbc.InputGroupText('ø 1 length'),
                                                dbc.Input(id='d1_l_multi',type='number', value= 40, min=20, max=150),
                                                dbc.InputGroupText('Step1 angle'),
                                                dbc.Input(id='d1_step',type='number', value = 90, min=30, max=180),
                                                ],size='sm',), style={'display':'block'}),
            html.Div(id='d2_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 2'),
                                                dbc.Input(id='d2',type='number',value = 12, min=3, max=35),
                                                dbc.InputGroupText('ø 2 length'),
                                                dbc.Input(id='d2_l',type='number', value = 60, min=20, max=150),
                                                # dbc.InputGroupText('Step2 angle'),
                                                # dbc.Input(id='d2_step',type='number', value = 180, min=30, max=180)
                                                ],size='sm',), style={'display':'block'}),
            html.Div(id='d2_details_multi',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 2'),
                                                dbc.Input(id='d2_multi',type='number',value = 12, min=3, max=35),
                                                dbc.InputGroupText('ø 2 length'),
                                                dbc.Input(id='d2_l_multi',type='number', value = 60, min=20, max=150),
                                                dbc.InputGroupText('Step2 angle'),
                                                dbc.Input(id='d2_step',type='number', value = 180, min=30, max=180)
                                                ],size='sm',), style={'display':'block'}),

            html.Div(id='d3_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 3'),
                                                dbc.Input(id='d3',type='number',value = 14, min=3, max=35), 
                                                dbc.InputGroupText('ø 3 length'),
                                                dbc.Input(id='d3_l',type='number',value =70 , min=20, max=150),
                                                # dbc.InputGroupText('Step3 angle'),
                                                # dbc.Input(id='d3_step',type='number', value = 180, min=30, max=180)
                                                ],size='sm',), style={'display':'block'}),

            html.Div(id='d4_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 4'),
                                                dbc.Input(id='d4',type='number', min=3, max=35), 
                                                dbc.InputGroupText('ø 4 length'),
                                                dbc.Input(id='d4_l',type='number', min=20, max=150)
                                                ],size='sm',), style={'display':'block'}),
            html.Div(id='d5_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 5 '),
                                                dbc.Input(id='d5',type='number', min=3, max=35), 
                                                dbc.InputGroupText('ø 5 length'),
                                                dbc.Input(id='d5_l',type='number', min=20, max=150)
                                                ],size='sm',), style={'display':'block'}),
            
            dbc.InputGroup([dbc.InputGroupText('FL'), 
                            dbc.Input(id= 'flute_l',type='number', value=50, min=3, max=200),
                            dbc.InputGroupText('OAL'),  
                            dbc.Input(id= 'oal',type='number', value=100, min=60, max=200)
                            ],size='sm'),

            dbc.InputGroup([dbc.InputGroupText('Shank ø '),
                             dbc.Input(id = 'shank_d', type='number', value=10),
                             ],size='sm'),
            html.Br(),
            dbc.Button('Preview', id='calculate'), 
            dbc.Button('DXF', id='drawing_download'),
            dbc.Button('PDF', id='drawing_pdf'),
            
         ]   

column2 = [
    # html.Br(),
    html.Div(id='graph_preview'),
    dcc.Download(id="download_drawing"),
]
 
########################################################################################################################################

app.layout =  dbc.Container(children=[
                    html.Br(),
                    html.Img(src="https://www.accuromm-ce.com/wp-content/uploads/2016/11/logo.png", alt="logo", height="40px"),
                    html.H4('Drill configurator'),
                    html.Br(),
                    dbc.Row([
                        #dbc.Col(column1, width=2,),
                        dbc.Col(column1, width=3,),
                        #dbc.Col(column3, width=3,),
                        dbc.Col(column2, width= 8,),
                        
                        ], style = {  'border': '1px outset black',  'border-radius': '5px'}
                    ),
                    # dbc.Row(
                    #     dbc.Col(html.Div(id='graph'), width= 8,),
                    # ),
], fluid=True)
# Widzialność w zalezności od wybranej ilości średnic   
@app.callback(
    Output('d1_details', 'style'),
    Output('d1_details_multi', 'style'),
    Output('d2_details', 'style'),
    Output('d2_details_multi', "style"),
    Output('d3_details', 'style'),
    Output('d4_details', 'style'),
    Output('d5_details', 'style'),
    Input('s_steps', 'value'),
)
def change_visibility(s_steps):
    visible = {'display':'block'}
    not_visible = {'display':'none'}
    
    if s_steps == 1:
        return {'display':'block'}, {'display':'none'}, {'display':'none'}, not_visible,{'display':'none'}, {'display':'none'}, {'display':'none'}
    elif s_steps == 2:
        return {'display':'none'}, {'display':'block'}, {'display':'block'}, not_visible, {'display':'none'}, {'display':'none'}, {'display':'none'}
    elif s_steps == 3:
        return {'display':'none'},{'display':'block'},  not_visible, visible,{'display':'block'}, {'display':'none'}, {'display':'none'}
    elif s_steps == 4:
        return {'display':'none'}, {'display':'block'}, {'display':'block'}, visible,{'display':'block'}, {'display':'block'}, {'display':'none'}
    elif s_steps == 5:
        return {'display':'none'}, {'display':'block'}, {'display':'block'}, visible, {'display':'block'}, {'display':'block'}, {'display':'block'}    



# ########################################################################################################################################
# @callback(
#     Output('output', 'children'),
#     Input('calculate', 'n_clicks'),
#     State('s_steps', 'value'),
#     State('d1', 'value'),
#     State('d1_l', 'value'),
#     State('d2', 'value'),
#     State('d2_l', 'value'),
    
# )
# def verify_input(n_clicks, s_steps, d1, d1_l, d2, d2_l): 
#     if n_clicks is None or n_clicks == 0:
#         raise PreventUpdate

#     if s_steps == 1:
#         text =  f' {d1=} '
#     elif s_steps == 2: 
#         text = f' {d1=}, {d2=}'
#     else: 
#         text = 'Check your input'
#     return text


# Profile preview using graph

@app.callback(
    Output('graph_preview', 'children'),
    Input('calculate', 'n_clicks'),
    State('s_steps', 'value'),
    State('d1', 'value'),
    State('d1_l', 'value'),
    State('d1_multi', 'value'),
    State('d1_l_multi', 'value'),
    State('d1_step', 'value'),
    State('d2', 'value'),
    State('d2_l', 'value'),
    State('d2_step', 'value'),
    State('d3', 'value'),
    State('d3_l', 'value'),
    State('shank_d', 'value'),
    State('oal', 'value'),
    State('point_angle', 'value'),
    State('flute_l', 'value'),
    
)
def graph(n_clicks, s_steps, d1, d1_length,
                            d1_multi, d1_length_multi, d1_step, 
                            d2, d2_length, d2_step ,
                            d3, d3_length, 
                            shank_d, oal, point, flute_l): 

    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate

    cordinates = Drawing()  
    if s_steps == 1:
        points = cordinates.add_profile_one(d1, d1_length, shank_d, oal, point)
        x = [i[0] for i in points]
        y = [i[1] for i in points]

    elif s_steps == 2: 
        points = cordinates.add_profile_two(d1_multi, d1_length_multi, d1_step, d2, d2_length,  shank_d, oal, point)
        x = [i[0] for i in points]
        y = [i[1] for i in points]

    elif s_steps == 3: 
        points = cordinates.add_profile_three(d1, d1_length,d2, d2_length,d3, d3_length, shank_d, oal, point)
        x = [i[0] for i in points]
        y = [i[1] for i in points]

    else: 
        x = [1,2,3]
        y = [1,2,3]

    # Flute position , 
    if s_steps ==1:
        if flute_l in range(0,d1_length):
            flute_dia = d1/2
        else: 
            flute_dia = shank_d/2
    if s_steps == 2:
        if flute_l in range(0,d1_length):
            flute_dia = d1/2
        elif  flute_l in range(d1_length, d2_length) :
            flute_dia = d2/2
        else: 
            flute_dia = shank_d/2
    if s_steps ==3:
        if flute_l in range(0,d1_length):
            flute_dia = d1/2
        elif  flute_l in range(d1_length, d2_length) :
            flute_dia = d2/2
        elif flute_l in range(d2_length, d3_length):
            flute_dia = d3/2
        else: 
            flute_dia = shank_d/2
        



    fig = go.Figure()
    fig.add_trace(go.Scatter(x =x , y= y, name="Tool Profile")) # Profil narzędzia / 'tonexty' , fill='tozeroy',
    fig.add_trace(go.Scatter(x = x[-4:], y = y[-4:], name= 'Shank'))
    fig.add_trace(go.Scatter(x=[flute_l, flute_l], y=[0, flute_dia], name="Flute"))
    # fig = px.line(x=x, y = y)
    fig.update_layout(template = 'plotly_dark',)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    fig.update_yaxes(scaleanchor = "x", scaleratio = 1,)
    fig.update_layout(yaxis_range=[0,20])
    # fig.add_annotation(x=2, y=5,
    #         text="Text annotation with arrow",
    #         showarrow=True,
    #         arrowhead=1)

    return dcc.Graph(figure=fig,)



@app.callback(
    Output('download_drawing', 'data'),
    Input('drawing_download', 'n_clicks'),
    Input('drawing_pdf', 'n_clicks'),
    State('s_steps', 'value'),
    State('d1', 'value'),
    State('d1_l', 'value'),
    State('d1_multi', 'value'),
    State('d1_l_multi', 'value'),
    State('d1_step', 'value'),
    State('d2', 'value'),
    State('d2_l', 'value'),
    State('d2_step', 'value'),
    State('d3', 'value'),
    State('d3_l', 'value'),
    State('shank_d', 'value'),
    State('oal', 'value'),
    State('point_angle', 'value'),
    State('flute_l', 'value'),
    
)
def download_drawing(n_clicks, n_clicks_2,  s_steps, d1, d1_length,d1_multi, d1_length_multi, d1_step, d2, d2_length, d2_step ,d3, d3_length, shank_d, oal, point, flute_l): 
    ''' Funkcja genereuje rysunek narzędzia w formacie .dxf oraz .pdf 
        '''
    ctx = dash.callback_context
    input_id = ctx.triggered[0]["prop_id"].split(".")[0]
    
    # if n_clicks is None or n_clicks_2 is None:
    #     raise PreventUpdate

    
    drawing = Drawing()
    if s_steps == 1:
        drawing.add_profile_one(d1, d1_length, shank_d, oal, point) 
    elif s_steps == 2: 
        drawing.add_profile_two(d1_multi, d1_length_multi, d1_step, d2, d2_length,  shank_d, oal, point)
    elif s_steps == 3: 
        drawing.add_profile_three(d1, d1_length,d2, d2_length,d3, d3_length, shank_d, oal, point)
    
    drawing.add_frame()
    #drawing.add_endface(d1)
    
    drawing.save('testowyplik')
    
    print(input_id)
    if input_id == 'drawing_download':
        return dcc.send_file(f'testowyplik.dxf')

    elif input_id == 'drawing_pdf':
        return dcc.send_file(f'testowyplik.pdf')



if __name__ == "__main__":
    # app.run_server(debug=True, host = '0.0.0.0' ,port=1112)
    app.run_server(debug=True,)