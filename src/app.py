import dash 
import dash_bootstrap_components as dbc
from dash import html, dcc, callback , Input , Output, State
from dash.exceptions import PreventUpdate
import ezdxf
import plotly.graph_objects as go
from step_profile import Step_profile
from drawing import Drawing
from ezdxf.addons.drawing import matplotlib

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
                                                dbc.Checkbox(id="standalone-checkbox",value=True,)
                                                ],size='sm',), style={'display':'block'}),
            html.Div(id='d2_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 2'),
                                                dbc.Input(id='d2',type='number',value = 12, min=3, max=35),
                                                dbc.InputGroupText('ø 2 length'),
                                                dbc.Input(id='d2_l',type='number', value = 60, min=20, max=150),
                                                dbc.InputGroupText('Step angle'),
                                                dbc.Input(id='d2_step',type='number', value = 90, min=30, max=180)
                                                ],size='sm',), style={'display':'block'}),

            html.Div(id='d3_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 3'),
                                                dbc.Input(id='d3',type='number',value = 14, min=3, max=35), 
                                                dbc.InputGroupText('ø 3 length'),
                                                dbc.Input(id='d3_l',type='number',value =70 , min=20, max=150),
                                                dbc.InputGroupText('Step angle'),
                                                dbc.Input(id='d3_step',type='number', value = 90, min=30, max=180)
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
            dbc.Button('test', id='test_btn'),
         ]   

column2 = [
    # html.Br(),
    html.Div(id='graph_preview'),
    dcc.Download(id="download_drawing"),
    dcc.Download(id="test"),
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
    Output('d2_details', 'style'),
    Output('d3_details', 'style'),
    Output('d4_details', 'style'),
    Output('d5_details', 'style'),
    Input('s_steps', 'value'),
)
def change_visibility(s_steps):
    if s_steps == 1:
        return {'display':'block'},  {'display':'none'}, {'display':'none'}, {'display':'none'}, {'display':'none'}
    elif s_steps == 2:
        return {'display':'block'},  {'display':'block'}, {'display':'none'}, {'display':'none'}, {'display':'none'}
    elif s_steps == 3:
        return {'display':'block'},  {'display':'block'}, {'display':'block'}, {'display':'none'}, {'display':'none'}
    elif s_steps == 4:
        return {'display':'block'},  {'display':'block'}, {'display':'block'}, {'display':'block'}, {'display':'none'}
    elif s_steps == 5:
        return {'display':'block'},  {'display':'block'}, {'display':'block'}, {'display':'block'}, {'display':'block'}    



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
def graph(n_clicks, s_steps, d1, d1_length, d2, d2_length, d2_step ,d3, d3_length, shank_d, oal, point, flute_l): 
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate

    cordinates = Drawing()  
    if s_steps == 1:
        points = cordinates.add_profile_one(d1, d1_length, shank_d, oal, point)
        x = [i[0] for i in points]
        y = [i[1] for i in points]

    elif s_steps == 2: 
        points = cordinates.add_profile_two(d1, d1_length,d2, d2_length, d2_step, shank_d, oal, point)
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

    return dcc.Graph(figure=fig,)



@app.callback(
    Output('download_drawing', 'data'),
    Input('drawing_download', 'n_clicks'),
    State('s_steps', 'value'),
    State('d1', 'value'),
    State('d1_l', 'value'),
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
def download_drawing(n_clicks, s_steps, d1, d1_length, d2, d2_length, d2_step, d3, d3_length, shank_d, oal, point, flute_l): 
    ''' Funkcja genereuje rysunek narzędzia w formacie .dxf oraz .pdf 
        '''
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate

    cordinates = Step_profile()  
    if s_steps == 1:
        points = cordinates.one_step(d1, d1_length, shank_d, oal, point)
      
    elif s_steps == 2: 
        points = cordinates.two_steps(d1, d1_length,d2, d2_length, d2_step, shank_d, oal, point)
    elif s_steps == 3: 
        points = cordinates.three_steps(d1, d1_length,d2, d2_length,d3, d3_length, shank_d, oal, point)
    else: 
        x = [1,2,3]
        y = [1,2,3]

    doc = ezdxf.new('R2000')
    # doc.layout().page_setup(size=(420, 297), margins=(10, 10, 10, 10), units="mm")
    
    msp = doc.modelspace()
    
    doc.layers.add(name="MyLines", color=7, linetype="DASHED")

    # profile 
    profile = doc.blocks.new(name= 'PROFILE')
    profile.add_lwpolyline(points)
    profile.add_line((points[0][0] - 1 ,0) , (oal+2,0), dxfattribs={'layer':'MyLines'})
    profile.add_lwpolyline(points).scale(1, -1, 1)

    # profile dimensions
    dim = profile.add_aligned_dim(p1=(points[1]), p2=(oal,d1 / 2), distance=30, override={'dimtad': 2, 'dimasz': 2, 'dimtxt': 2}) #oal
    dim1 = profile.add_aligned_dim(p1=(points[1]), p2=(points[2]), distance=15, override={'dimtad': 2,'dimasz': 2,'dimtxt': 2})           #d1 length
    dim2 = profile.add_aligned_dim(p1=(points[1]), p2=(( points[1][0], -points[1][1])), distance=-10, override={'dimtad': 2, 'dimasz': 2, 'dimtxt': 2, 'dimjust':1}) # d1 
    dim3 = profile.add_aligned_dim(p1=(points[-3]), p2=(( points[-3][0], -points[-3][1])), distance=10, override={'dimtad': 2, 'dimasz': 2, 'dimtxt': 2, 'dimjust':1})# shank diameter
    # dim3 = msp.add_aligned_dim(p1=(p5), p2=(p5a), distance=10, override={'dimtad': 2,'dimasz': 2, 'dimtxt': 2})          #shank d
    # dim4 = msp.add_linear_dim(base= (3,2) ,p1=(p5), p2=(p5a), angle=-270, override={'dimtad': 2,'dimasz': 2, 'dimtxt': 2})  

    dimensions = [dim, dim1, dim2]
    for item in dimensions:
        item.render() 

    # tip view
    tip = doc.blocks.new(name = 'TIP')

    tip.add_circle((0,0), d1/2)

    # frame
    try: 
        frame_a4 = ezdxf.readfile('a4.DXF')
    except: 
        frame_a4 = ezdxf.readfile('src/a4.DXF')

    frame_ent = frame_a4.entities
    frame = doc.blocks.new(name = 'FRAME')
     
    for i in frame_ent: 
        #print(i)
        frame.add_foreign_entity(i)

    # adding blocks to modelspace
    msp.add_blockref('PROFILE', (-20,0))
    msp.add_blockref('TIP', (-70,0))
    msp.add_blockref('FRAME', (0,0))

    doc.saveas(f'drawing.dxf')
    matplotlib.qsave(doc.modelspace(), f'drawing.pdf',dpi=100, bg='#FFFFFF')

    return dcc.send_file(f'drawing.dxf')


###############################

@app.callback(
    Output('test', 'data'),
    Input('test_btn', 'n_clicks'),
    State('s_steps', 'value'),
    State('d1', 'value'),
    State('d1_l', 'value'),
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
def download_drawing(n_clicks, s_steps, d1, d1_length, d2, d2_length, d2_step, d3, d3_length, shank_d, oal, point, flute_l): 
    ''' Funkcja genereuje rysunek narzędzia w formacie .dxf oraz .pdf 
        '''
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate

    
    drawing = Drawing()
    if s_steps == 1:
        drawing.add_profile_one(d1, d1_length, shank_d, oal, point) 
    elif s_steps == 2: 
        drawing.add_profile_two(d1, d1_length,d2, d2_length, d2_step, shank_d, oal, point)
    elif s_steps == 3: 
        drawing.add_profile_three(d1, d1_length,d2, d2_length,d3, d3_length, shank_d, oal, point)
    
    drawing.add_frame()
    drawing.add_endface(d1)
    
    drawing.save('testowyplik')

    return dcc.send_file(f'testowyplik.dxf')



if __name__ == "__main__":
    # app.run_server(debug=True, host = '0.0.0.0' ,port=1112)
    app.run_server(debug=True,)