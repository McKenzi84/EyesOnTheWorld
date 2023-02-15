import dash 
import dash_bootstrap_components as dbc
from dash import html, dcc, callback , Input , Output, State
from dash.exceptions import PreventUpdate
import ezdxf
import plotly.graph_objects as go
from step_profile import Step_profile

app = dash.Dash(external_stylesheets=[dbc.themes.SLATE])
server = app.server

border = {  'border': '1px outset black',  'border-radius': '5px'}

# Zawartość drop-dałnów

tool_type = ['TFH Drill', 'TFS Drill', 'GK drill',]
cutting_edges = [2,3,4,5,6]
steps = [1,2,3,]
material = ['Unground bar', 'Ground bar', 'Spacial blank']
material_coolant = ['Ground helical coolant - 30°','Ground helical coolant - 40°']
coatings = ['Triple Cr', 'Triple Si', 'Alcrona', 'DLC', 'None']
#afc_prices = pd.read_excel('assets/afc_prices.xlsx')# Feedrates: 
# TFH_FEED = 5
# TFS_FEED = 10
# GK_FEED = 5


# column1 = [     html.Br(),
#                 html.H6('1. Basic info '),
#                 dcc.Dropdown(id='s_type',options=[{'label': x, 'value': (x)} for x in tool_type],style={'color':'black', 'width': '100%'},placeholder="Select tool type",value="TFH Drill"),
#                 dcc.Dropdown(id='s_edges',options=[{'label':f' {x} Z' , 'value': (x)} for x in cutting_edges],style={'color':'black', 'width': '100%'},placeholder="How many cutting edges",value=2),
#                 dcc.Dropdown(id='s_steps',options=[{'label': f' {x} Steps', 'value': (x)} for x in steps],style={'color':'black', 'width': '100%'},placeholder="How many steps", value=1),
#                 #dcc.Dropdown(id='s_material',options=[{'label': x, 'value': (x)} for x in material],style={'color':'black', 'width': '100%'},placeholder="Material type to be used",),
#                 dcc.Dropdown(id='s_coating',options=[{'label': f'{x} Coating', 'value': (x)} for x in coatings],style={'color':'black', 'width': '100%'},placeholder="Coating type",),
#                 html.Div(id='output'),
#             ]


column1 = [ html.Br(),
            html.H6('1. Tool info'),
            dcc.Dropdown(id='s_steps',options=[{'label': f' {x} Diameter', 'value': (x)} for x in steps],style={'color':'black', 'width': '100%'},placeholder="How many diameters", value=1),
            dbc.InputGroup([
                    dbc.InputGroupText('Point angle °'), dbc.Input(id= 'point_angle',type='number', value=135), dbc.InputGroupText('Helix °'),  dbc.Input(id= 'helix_angle',type='number', value=30),],size='sm'),                                              
            html.Div(id='d1_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 1'),dbc.Input(id='d1',type='number', value=10), dbc.InputGroupText('ø 1 length'),dbc.Input(id='d1_l',type='number', value= 50),
                    dbc.Checkbox(id="standalone-checkbox",value=True,)
                     ],size='sm',),
                    style={'display':'block'}),
            html.Div(id='d2_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 2'),dbc.Input(id='d2',type='number'), dbc.InputGroupText('ø 2 length'),dbc.Input(id='d2_l',type='number')],size='sm',),
                    style={'display':'block'}),
            html.Div(id='d3_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 3'),dbc.Input(id='d3',type='number'), dbc.InputGroupText('ø 3 length'),dbc.Input(id='d3_l',type='number')],size='sm',),
                    style={'display':'block'}),
            html.Div(id='d4_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 4'),dbc.Input(id='d4',type='number'), dbc.InputGroupText('ø 4 length'),dbc.Input(id='d4_l',type='number')],size='sm',),
                    style={'display':'block'}),
            html.Div(id='d5_details',
                    children = dbc.InputGroup([dbc.InputGroupText('ø 5 '),dbc.Input(id='d5',type='number'), dbc.InputGroupText('ø 5 length'),dbc.Input(id='d5_l',type='number')],size='sm',),
                    style={'display':'block'}),
            
            dbc.InputGroup([dbc.InputGroupText('FL'), dbc.Input(id= 'flute_l',type='number', value=50), dbc.InputGroupText('OAL'),  dbc.Input(id= 'oal',type='number', value=100)],size='sm'),
            dbc.InputGroup([dbc.InputGroupText('Shank ø '), dbc.Input(id = 'shank_d', type='number', value=10),],size='sm'),
            html.Br(),
            dbc.Button('Preview', id='calculate'), 
            dbc.Button('Drawing', id='drawing_download'),
         ]   

column2 = [
    html.Br(),
    html.Div(id='graph_preview'),
    dcc.Download(id="download_drawing"),
]
# column3 = [ html.Br(),
#             html.H6('3. Material info'),
#             dcc.Dropdown(id='bar_type',options=[{'label': x, 'value': (x)} for x in material_coolant],style={'color':'black', 'width': '100%'},placeholder="Type",),
#             dcc.Dropdown(id='bar_length',options=[310,330,415],style={'color':'black', 'width': '100%'},placeholder="Bar length",),
#             html.Div(id= 'material_details'),
#             html.Br(),
#             dbc.InputGroup([dbc.InputGroupText(' ø '),dbc.Input(id='material_d',type='number', value=10), dbc.InputGroupText('Length'),dbc.Input(id='material_l',type='number', value=105)],size='sm')
#             ]    

# column4 = [ html.Br(),
#             html.H6('4. Grinding time'),
#             html.Div(id='cost_break')
#             ]     
########################################################################################################################################

app.layout =  dbc.Container(children=[
                    html.H3('Drawing generator'),
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


# Profile preview 

@app.callback(
    Output('graph_preview', 'children'),
    Input('calculate', 'n_clicks'),
    State('s_steps', 'value'),
    State('d1', 'value'),
    State('d1_l', 'value'),
    State('d2', 'value'),
    State('d2_l', 'value'),
    State('d3', 'value'),
    State('d3_l', 'value'),
    State('shank_d', 'value'),
    State('oal', 'value'),
    State('point_angle', 'value'),
    State('flute_l', 'value'),
    
)
def graph(n_clicks, s_steps, d1, d1_length, d2, d2_length,d3, d3_length, shank_d, oal, point, flute_l): 
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate

    cordinates = Step_profile()  
    if s_steps == 1:
        x, y, z = cordinates.one_step(d1, d1_length, shank_d, oal, point)
    elif s_steps == 2: 
        x, y = cordinates.two_steps(d1, d1_length,d2, d2_length, shank_d, oal, point)
    elif s_steps == 3: 
        x, y = cordinates.three_steps(d1, d1_length,d2, d2_length,d3, d3_length, shank_d, oal, point)
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
    fig.update_yaxes(scaleanchor = "x", scaleratio = 1,)

    return dcc.Graph(figure=fig,)



@app.callback(
    Output('download_drawing', 'data'),
    Input('drawing_download', 'n_clicks'),
    State('s_steps', 'value'),
    State('d1', 'value'),
    State('d1_l', 'value'),
    State('d2', 'value'),
    State('d2_l', 'value'),
    State('d3', 'value'),
    State('d3_l', 'value'),
    State('shank_d', 'value'),
    State('oal', 'value'),
    State('point_angle', 'value'),
    State('flute_l', 'value'),
    
)
def download_drawing(n_clicks, s_steps, d1, d1_length, d2, d2_length,d3, d3_length, shank_d, oal, point, flute_l): 
    if n_clicks is None or n_clicks == 0:
        raise PreventUpdate

    cordinates = Step_profile()  
    if s_steps == 1:
        x, y, z = cordinates.one_step(d1, d1_length, shank_d, oal, point)
    elif s_steps == 2: 
        x, y = cordinates.two_steps(d1, d1_length,d2, d2_length, shank_d, oal, point)
    elif s_steps == 3: 
        x, y = cordinates.three_steps(d1, d1_length,d2, d2_length,d3, d3_length, shank_d, oal, point)
    else: 
        x = [1,2,3]
        y = [1,2,3]

    doc = ezdxf.new('R2000')
    msp = doc.modelspace()

    # profile 
    profile = doc.blocks.new(name= 'PROFILE')
    profile.add_lwpolyline(z)
    profile.add_line((0,0) , (oal,0))
    profile.add_lwpolyline(z).scale(1, -1, 1)

    # tip view
    tip = doc.blocks.new(name = 'TIP')
    tip.add_circle((0,0), d1/2)

    # frame
    frame_a4 = ezdxf.readfile('a4.DXF')
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

    return dcc.send_file(f'drawing.dxf')


if __name__ == "__main__":
    # app.run_server(debug=True, host = '0.0.0.0' ,port=1112)
    app.run_server(debug=True,)