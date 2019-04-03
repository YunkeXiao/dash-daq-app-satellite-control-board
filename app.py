import random
import time
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import State, Input, Output
import dash_daq as daq

app = dash.Dash(__name__)

# This is for Heroku
server = app.server

# CSS Imports
external_css = ['./assets/style.css']

for css in external_css:
    app.css.append_css({"external_url": css})

##############################################################################################################
# Side panel
##############################################################################################################

satellite_dropdown = dcc.Dropdown(
    id='satellite-dropdown-component',
    options=[
        {
            'label': 'H45-K1',
            'value': 'h45-k1'
        },
        {
            'label': 'L12-5',
            'value': 'l12-5'
        },
    ],
    clearable=False,
    # value='h45-k1',
    style={
        'color': '#017e84',
        'text-align': 'center',
        'cursor': 'pointer'
    }
)

satellite_dropdown_text = html.P(
    id='satellite-dropdown-text',
    children=['Satellite Dashboard']
)

satellite_title = html.H1(
    id='satellite-name',
    children="")

satellite_body = html.P(
    className='satellite-description',
    id='satellite-description',
    children=[
        ""
    ]
)

side_panel_layout = html.Div(
    id='panel-side',
    children=[
        satellite_dropdown_text,
        html.Div(
            id='satellite-dropdown',
            children=[
                satellite_dropdown,
            ]
        ),
        html.Div(
            id='panel-side-text',
            children=[
                satellite_title,
                satellite_body
            ]
        )
    ],
)


##############################################################################################################
# Satellite location tracker
##############################################################################################################

# Helper to straighten lines on the map
def flatten_path(xy1, xy2):
    diff_rate = (xy2 - xy1) / 100
    res_list = []
    for i in range(100):
        res_list.append(xy1 + i * diff_rate)
    return res_list


map_data = [
    {
        'type': 'scattergeo',
        'lat': [],
        'lon': [],
        'hoverinfo': 'none',
        'mode': 'lines',
        'line': {
            'width': 2,
            'color': '#017e84',
        }
    },
    {
        'type': 'scattergeo',
        'lat': [0],
        'lon': [0],
        'hoverinfo': 'text+lon+lat',
        'text': 'Current Position',
        'mode': 'markers',
        'marker': {
            'size': 10,
            'color': 'black'
        }
    }
]

map_layout = {
    'geo': {
        'showframe': False,
        'showcoastlines': False,
        'showland': True,
        'showocean': True,
        'resolution': 100,
        'landcolor': 'white',
        'oceancolor': '#e8e3df',
        'scope': 'world',
        'showgrid': True,

    },
    'width': 865,
    'height': 610,
    'showlegend': False
}

map_graph = dcc.Graph(
    id='world-map',
    figure={
        'data': map_data,
        'layout': map_layout
    },
    config={
        'displayModeBar': False,
        'scrollZoom': False,
    }
)

##############################################################################################################
# Histogram
##############################################################################################################

histogram = dcc.Graph(
    id='graph-panel',
    figure={
        'data': [{
            'x': [i for i in range(60)],
            'y': [i for i in range(60)],
            'type': 'scatter',
            'marker': {
                'color': 'white',
            }
        }],
        'layout': {
            'title': 'Select A Propriety To Display',
            'width': 400,
            'height': 350,
            'margin': {
                'l': 35,
                'r': 70,
                't': 100,
                'b': 45
            },
            'xaxis': {
                'dtick': 5,
                'gridcolor': '#999999',
            },
            'yaxis': {
                'gridcolor': '#999999',
            },
            'plot_bgcolor': '#017e84',
            'paper_bgcolor': '#017e84',
            'font': {
                'color': 'white'
            },
        }
    },
    config={
        'displayModeBar': False
    }
)

##############################################################################################################
# Dash_DAQ elements
##############################################################################################################

utc = html.Div(
    id='control-panel-utc',
    children=[
        daq.LEDDisplay(
            id='control-panel-utc-component',
            value="16:23",
            label='Time',
            size=54,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

speed = html.Div(
    id='control-panel-speed',
    children=[
        daq.Gauge(
            id='control-panel-speed-component',
            label='Speed',
            min=0,
            max=40,
            showCurrentValue=True,
            value=27.859,
            units='1000km/h',
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

elevation = html.Div(
    id='control-panel-elevation',
    children=[
        daq.Tank(
            id='control-panel-elevation-component',
            label='Elevation',
            min=0,
            max=1000,
            value=650,
            units='kilometers',
            showCurrentValue=True,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

temperature = html.Div(
    id='control-panel-temperature',
    children=[
        daq.Tank(
            id='control-panel-temperature-component',
            label='Temperature',
            min=0,
            max=500,
            value=290,
            units='Kelvin',
            showCurrentValue=True,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

fuel_indicator = html.Div(
    id='control-panel-fuel',
    children=[
        daq.GraduatedBar(
            id='control-panel-fuel-component',
            label='Fuel-Level',
            min=0,
            max=100,
            value=76,
            step=1,
            showCurrentValue=True,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

battery_indicator = html.Div(
    id='control-panel-battery',
    children=[
        daq.GraduatedBar(
            id='control-panel-battery-component',
            label='Battery-Level',
            min=0,
            max=100,
            value=85,
            step=1,
            showCurrentValue=True,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

longitude = html.Div(
    id='control-panel-longitude',
    children=[
        daq.LEDDisplay(
            id='control-panel-longitude-component',
            value="0000.0000",
            label='Longitude',
            size=24,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

latitude = html.Div(
    id='control-panel-latitude',
    children=[
        daq.LEDDisplay(
            id='control-panel-latitude-component',
            value="0050.9789",
            label='Latitude',
            size=24,
            color='#017e84',
            style={
                'color': '#black'
            }
        )
    ],
    n_clicks=0
)

solar_panel_0 = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-solar-panel-0',
    label='Solar-Panel-0',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

solar_panel_1 = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-solar-panel-1',
    label='Solar-Panel-1',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

camera = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-camera',
    label='Camera',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

thrusters = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-thrusters',
    label='Thrusters',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

motor = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-motor',
    label='Motor',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

communication_signal = daq.Indicator(
    className='panel-lower-indicator',
    id='control-panel-communication-signal',
    label='Signal',
    labelPosition='bottom',
    value=True,
    color='#017e84',
    style={
        'color': '#black'
    }
)

map_toggle = daq.ToggleSwitch(
    id='control-panel-toggle-map',
    value=True,
    label='Show Satellite Path',
    color='#017e84',
    style={
        'color': '#black'
    }
)

minute_toggle = daq.ToggleSwitch(
    id='control-panel-toggle-minute',
    value=True,
    label='Past Hour - Past Minute',
    color='#017e84',
    style={
        'color': '#black'
    }
)

###############################################################################################################
# Control panel + map
##############################################################################################################
main_panel_layout = html.Div(
    id='panel-upper-lower',
    children=[
        html.P(
            id='placeholder',
            children=[0]
        ),
        dcc.Interval(
            id='interval',
            interval=1 * 2000,
            n_intervals=0
        ),
        html.Div(
            id='panel-upper',
            children=[
                map_graph,
                histogram,
            ]
        ),
        html.Div(
            id='panel-lower',
            children=[
                html.Div(
                    id='panel-lower-top-break',
                    children=[
                        map_toggle,
                        minute_toggle
                    ]
                ),
                html.Div(
                    id='panel-lower-0',
                    children=[
                        elevation,
                        temperature,
                        speed,
                        utc,
                    ]
                ),
                html.Div(
                    id='panel-lower-1',
                    children=[
                        html.Div(
                            id='panel-lower-led-displays',
                            children=[
                                latitude,
                                longitude,
                            ]
                        ),
                        html.Div(
                            id='panel-lower-indicators',
                            children=[
                                html.Div(
                                    id='panel-lower-indicators-0',
                                    children=[
                                        solar_panel_0,
                                        thrusters,
                                    ]
                                ),
                                html.Div(
                                    id='panel-lower-indicators-1',
                                    children=[
                                        solar_panel_1,
                                        motor,
                                    ]
                                ),
                                html.Div(
                                    id='panel-lower-indicators-2',
                                    children=[
                                        camera,
                                        communication_signal
                                    ]
                                ),
                            ]
                        ),
                        html.Div(
                            id='panel-lower-graduated-bars',
                            children=[
                                fuel_indicator,
                                battery_indicator
                            ]
                        ),
                    ]
                ),
            ]
        )
    ],
)

##############################################################################################################
# Root
##############################################################################################################
root_layout = html.Div(
    id='root',
    children=[
        side_panel_layout,
        main_panel_layout
    ]
)

app.layout = root_layout

##############################################################################################################
# Callbacks Data
##############################################################################################################

# Check which graph should be displayed
previous_states = {
    'elevation': 0,
    'temperature': 0,
    'speed': 0,
    'latitude': 0,
    'longitude': 0,
    'fuel': 0,
    'battery': 0,
}

# For the case no components were clicked, we need to know what type of graph to preserve
data_type = ""

# Pandas
df_non_gps_h = pd.read_csv('./data/non_gps_data_h.csv')
df_non_gps_m = pd.read_csv('./data/non_gps_data_m.csv')
df_gps_m = pd.read_csv('./data/gps_data_m.csv')
df_gps_h = pd.read_csv('./data/gps_data_h.csv')

# Satellite H45-K1 data
df_non_gps_h_0 = pd.read_csv('./data/non_gps_data_h_0.csv')
df_non_gps_m_0 = pd.read_csv('./data/non_gps_data_m_0.csv')
df_gps_m_0 = pd.read_csv('./data/gps_data_m_0.csv')
df_gps_h_0 = pd.read_csv('./data/gps_data_h_0.csv')

# Satellite L12-5 data
df_non_gps_h_1 = pd.read_csv('./data/non_gps_data_h_1.csv')
df_non_gps_m_1 = pd.read_csv('./data/non_gps_data_m_1.csv')
df_gps_m_1 = pd.read_csv('./data/gps_data_m_1.csv')
df_gps_h_1 = pd.read_csv('./data/gps_data_h_1.csv')

# Used for the hour mode graph data
hour_data = {
    'elevation': [df_non_gps_h['elevation'][i] for i in range(0, 60)],
    'temperature': [df_non_gps_h['temperature'][i] for i in range(0, 60)],
    'speed': [df_non_gps_h['speed'][i] for i in range(0, 60)],
    'latitude': ["{0:09.4f}".format(df_gps_h['lat'][i]) for i in range(0, 60)],
    'longitude': ["{0:09.4f}".format(df_gps_h['lon'][i]) for i in range(0, 60)],
    'fuel': [df_non_gps_h['fuel'][i] for i in range(0, 60)],
    'battery': [df_non_gps_h['battery'][i] for i in range(0, 60)],
}

# Used for the minute mode graph data
minute_data = {
    'elevation': [df_non_gps_m['elevation'][i] for i in range(0, 60)],
    'temperature': [df_non_gps_m['temperature'][i] for i in range(0, 60)],
    'speed': [df_non_gps_m['speed'][i] for i in range(0, 60)],
    'latitude': ["{0:09.4f}".format(df_gps_m['lat'][i]) for i in range(0, 60)],
    'longitude': ["{0:09.4f}".format(df_gps_m['lon'][i]) for i in range(0, 60)],
    'fuel': [df_non_gps_m['fuel'][i] for i in range(0, 60)],
    'battery': [df_non_gps_m['battery'][i] for i in range(0, 60)],
}

# Satellite H45-L1 data
hour_data_0 = {
    'elevation': [df_non_gps_h_0['elevation'][i] for i in range(0, 60)],
    'temperature': [df_non_gps_h_0['temperature'][i] for i in range(0, 60)],
    'speed': [df_non_gps_h_0['speed'][i] for i in range(0, 60)],
    'latitude': ["{0:09.4f}".format(df_gps_h_0['lat'][i]) for i in range(0, 60)],
    'longitude': ["{0:09.4f}".format(df_gps_h_0['lon'][i]) for i in range(0, 60)],
    'fuel': [df_non_gps_h_0['fuel'][i] for i in range(0, 60)],
    'battery': [df_non_gps_h_0['battery'][i] for i in range(0, 60)],
}

minute_data_0 = {
    'elevation': [df_non_gps_m_0['elevation'][i] for i in range(0, 60)],
    'temperature': [df_non_gps_m_0['temperature'][i] for i in range(0, 60)],
    'speed': [df_non_gps_m_0['speed'][i] for i in range(0, 60)],
    'latitude': ["{0:09.4f}".format(df_gps_m_0['lat'][i]) for i in range(0, 60)],
    'longitude': ["{0:09.4f}".format(df_gps_m_0['lon'][i]) for i in range(0, 60)],
    'fuel': [df_non_gps_m_0['fuel'][i] for i in range(0, 60)],
    'battery': [df_non_gps_m_0['battery'][i] for i in range(0, 60)],
}

# Satellite L12-5 data
hour_data_1 = {
    'elevation': [df_non_gps_h_1['elevation'][i] for i in range(0, 60)],
    'temperature': [df_non_gps_h_1['temperature'][i] for i in range(0, 60)],
    'speed': [df_non_gps_h_1['speed'][i] for i in range(0, 60)],
    'latitude': ["{0:09.4f}".format(df_gps_h_1['lat'][i]) for i in range(0, 60)],
    'longitude': ["{0:09.4f}".format(df_gps_h_1['lon'][i]) for i in range(0, 60)],
    'fuel': [df_non_gps_h_1['fuel'][i] for i in range(0, 60)],
    'battery': [df_non_gps_h_1['battery'][i] for i in range(0, 60)],
}

minute_data_1 = {
    'elevation': [df_non_gps_m_1['elevation'][i] for i in range(0, 60)],
    'temperature': [df_non_gps_m_1['temperature'][i] for i in range(0, 60)],
    'speed': [df_non_gps_m_1['speed'][i] for i in range(0, 60)],
    'latitude': ["{0:09.4f}".format(df_gps_m_1['lat'][i]) for i in range(0, 60)],
    'longitude': ["{0:09.4f}".format(df_gps_m_1['lon'][i]) for i in range(0, 60)],
    'fuel': [df_non_gps_m_1['fuel'][i] for i in range(0, 60)],
    'battery': [df_non_gps_m_1['battery'][i] for i in range(0, 60)],
}


# Add new data every second/minute
@app.callback(
    Output(component_id='placeholder', component_property='children'),
    [Input(component_id='interval', component_property='n_intervals')]
)
def update_data(interval):

    # Update H45-K1 data
    minute_data_0['elevation'].append(minute_data_0['elevation'][0])
    minute_data_0['elevation'] = minute_data_0['elevation'][1:61]
    minute_data_0['temperature'].append(minute_data_0['temperature'][0])
    minute_data_0['temperature'] = minute_data_0['temperature'][1:61]
    minute_data_0['speed'].append(minute_data_0['speed'][1])
    minute_data_0['speed'] = minute_data_0['speed']
    # Latitude and longitude minute and hour data are really the same
    minute_data_0['latitude'].append("{0:09.4f}".format(df_gps_m_0['lat'][60 + interval % 3600]))
    minute_data_0['latitude'] = minute_data_0['latitude'][1:61]
    minute_data_0['longitude'].append("{0:09.4f}".format(df_gps_m_0['lon'][60 + interval % 3600]))
    minute_data_0['longitude'] = minute_data_0['longitude'][1:61]
    minute_data_0['fuel'].append(minute_data_0['fuel'][0])
    minute_data_0['fuel'] = minute_data_0['fuel'][1:61]
    minute_data_0['battery'].append(minute_data_0['battery'][0])
    minute_data_0['battery'] = minute_data_0['battery'][1:61]

    if interval % 60 == 0:
        hour_data_0['elevation'].append(hour_data_0['elevation'][0])
        hour_data_0['elevation'] = hour_data_0['elevation'][1:61]
        hour_data_0['temperature'].append(hour_data_0['temperature'][0])
        hour_data_0['temperature'] = hour_data_0['temperature'][1:61]
        hour_data_0['speed'].append(hour_data_0['speed'][0])
        hour_data_0['speed'] = hour_data_0['speed'][1:61]
        hour_data_0['latitude'].append("{0:09.4f}".format(df_gps_h_0['lat'][interval % 60]))
        hour_data_0['latitude'] = hour_data_0['latitude'][1:61]
        hour_data_0['longitude'].append("{0:09.4f}".format(df_gps_h_0['lon'][interval % 60]))
        hour_data_0['longitude'] = hour_data_0['longitude'][1:61]
        hour_data_0['fuel'].append(hour_data_0['fuel'][0])
        hour_data_0['fuel'] = hour_data_0['fuel'][1:61]
        hour_data_0['battery'].append(hour_data_0['battery'][0])
        hour_data_0['battery'] = hour_data_0['battery']

    # Update L12-5 data
    minute_data_1['elevation'].append(minute_data_1['elevation'][0])
    minute_data_1['elevation'] = minute_data_1['elevation'][1:61]
    minute_data_1['temperature'].append(minute_data_1['temperature'][0])
    minute_data_1['temperature'] = minute_data_1['temperature'][1:61]
    minute_data_1['speed'].append(minute_data_1['speed'][1])
    minute_data_1['speed'] = minute_data_1['speed']
    # Latitude and longitude minute and hour data are really the same
    minute_data_1['latitude'].append("{0:09.4f}".format(df_gps_m_1['lat'][60 + interval % 3600]))
    minute_data_1['latitude'] = minute_data_1['latitude'][1:61]
    minute_data_1['longitude'].append("{0:09.4f}".format(df_gps_m_1['lon'][60 + interval % 3600]))
    minute_data_1['longitude'] = minute_data_1['longitude'][1:61]
    minute_data_1['fuel'].append(minute_data_1['fuel'][0])
    minute_data_1['fuel'] = minute_data_1['fuel'][1:61]
    minute_data_1['battery'].append(minute_data_1['battery'][0])
    minute_data_1['battery'] = minute_data_1['battery'][1:61]

    if interval % 60 == 0:
        hour_data_1['elevation'].append(hour_data_1['elevation'][0])
        hour_data_1['elevation'] = hour_data_1['elevation'][1:61]
        hour_data_1['temperature'].append(hour_data_1['temperature'][0])
        hour_data_1['temperature'] = hour_data_1['temperature'][1:61]
        hour_data_1['speed'].append(hour_data_1['speed'][0])
        hour_data_1['speed'] = hour_data_1['speed'][1:61]
        hour_data_1['latitude'].append("{0:09.4f}".format(df_gps_h_1['lat'][interval % 60]))
        hour_data_1['latitude'] = hour_data_1['latitude'][1:61]
        hour_data_1['longitude'].append("{0:09.4f}".format(df_gps_h_1['lon'][interval % 60]))
        hour_data_1['longitude'] = hour_data_1['longitude'][1:61]
        hour_data_1['fuel'].append(hour_data_1['fuel'][0])
        hour_data_1['fuel'] = hour_data_1['fuel'][1:61]
        hour_data_1['battery'].append(hour_data_1['battery'][0])
        hour_data_1['battery'] = hour_data_1['battery']
    return [0]


##############################################################################################################
# Callbacks Histogram
##############################################################################################################

# Update the graph
@app.callback(
    Output(component_id='graph-panel', component_property='figure'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='control-panel-toggle-minute', component_property='value'),
     Input(component_id='control-panel-elevation', component_property='n_clicks'),
     Input(component_id='control-panel-temperature', component_property='n_clicks'),
     Input(component_id='control-panel-speed', component_property='n_clicks'),
     Input(component_id='control-panel-latitude', component_property='n_clicks'),
     Input(component_id='control-panel-longitude', component_property='n_clicks'),
     Input(component_id='control-panel-fuel', component_property='n_clicks'),
     Input(component_id='control-panel-battery', component_property='n_clicks'),
     ]
)
def update_graph(interval, minute_mode, elevation_n_clicks, temperature_n_clicks, speed_n_clicks, latitude_n_clicks,
                 longitude_n_clicks, fuel_n_clicks, battery_n_clicks):
    # Used to check stuff
    global data_type

    # Decide the range of Y given if minute_mode is on
    def set_y_range(type):
        if type == 'elevation':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 1000],
                    'autorange': False
                }

        elif type == 'temperature':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 500],
                    'autorange': False
                }

        elif type == 'speed':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 40],
                    'autorange': False
                }

        elif type == 'latitude':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [-60, 60],
                    'autorange': False,
                }

        elif type == 'longitude':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 360],
                    'autorange': False,
                }

        elif type == 'fuel' or type == 'battery':
            if minute_mode:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'autorange': True
                }
            else:
                figure['layout']['yaxis'] = {
                    'rangemode': 'normal',
                    'range': [0, 100],
                    'autorange': False
                }

    # Function to update values
    def update_graph_data(type):
        global data_type
        data_type = type

        if minute_mode:
            figure['data'][0]['y'] = list(reversed(minute_data[type]))
        else:
            figure['data'][0]['y'] = list(reversed(hour_data[type]))

        # Title and scale differs
        if type == 'elevation':
            figure['layout']['title'] = 'Elevation Histogram'
        elif type == 'temperature':
            figure['layout']['title'] = 'Temperature Histogram'
        elif type == 'speed':
            figure['layout']['title'] = 'Speed Histogram'
        elif type == 'latitude':
            figure['layout']['title'] = 'Latitude Histogram'
        elif type == 'longitude':
            figure['layout']['title'] = 'Longitude Histogram'
        elif type == 'fuel':
            figure['layout']['title'] = 'Fuel Histogram'
        elif type == 'battery':
            figure['layout']['title'] = 'Battery Histogram'

    # A default figure option to base off everything else from
    figure = {
        'data': [{
            'x': [i for i in range(60)],
            'y': [i for i in range(60)],
            'type': 'scatter',
            'marker': {
                'color': 'white',
            }
        }],
        'layout': {
            'title': 'Select A Propriety To Display',
            'width': 400,
            'height': 350,
            'margin': {
                'l': 35,
                'r': 70,
                't': 100,
                'b': 45
            },
            'xaxis': {
                'dtick': 5,
                'gridcolor': '#999999',
            },
            'yaxis': {
                'gridcolor': '#999999',
            },
            'plot_bgcolor': '#017e84',
            'paper_bgcolor': '#017e84',
            'font': {
                'color': 'white'
            }
        }
    }

    # First pass checks if a component has been selected
    if elevation_n_clicks != previous_states['elevation']:
        previous_states['elevation'] += 1
        set_y_range('elevation')
        update_graph_data('elevation')

    elif temperature_n_clicks != previous_states['temperature']:
        previous_states['temperature'] += 1
        set_y_range('temperature')
        update_graph_data('temperature')

    elif speed_n_clicks != previous_states['speed']:
        previous_states['speed'] += 1
        set_y_range('speed')
        update_graph_data('speed')

    elif latitude_n_clicks != previous_states['latitude']:
        previous_states['latitude'] += 1
        update_graph_data('latitude')
        set_y_range('latitude')

    elif longitude_n_clicks != previous_states['longitude']:
        previous_states['longitude'] += 1
        set_y_range('longitude')
        update_graph_data('longitude')

    elif fuel_n_clicks != previous_states['fuel']:
        previous_states['fuel'] += 1
        set_y_range('fuel')
        update_graph_data('fuel')

    elif battery_n_clicks != previous_states['battery']:
        previous_states['battery'] += 1
        set_y_range('battery')
        update_graph_data('battery')

    # If no component has been selected, check for most recent data_type, to prevent graph from always resetting
    else:
        if data_type == 'elevation':
            set_y_range('elevation')
            update_graph_data('elevation')

        elif data_type == 'temperature':
            set_y_range('temperature')
            update_graph_data('temperature')

        elif data_type == 'speed':
            set_y_range('speed')
            update_graph_data('speed')

        elif data_type == 'latitude':
            set_y_range('latitude')
            update_graph_data('latitude')

        elif data_type == 'longitude':
            set_y_range('longitude')
            update_graph_data('longitude')

        elif data_type == 'fuel':
            set_y_range('fuel')
            update_graph_data('fuel')

        elif data_type == 'battery':
            set_y_range('battery')
            update_graph_data('battery')

        else:
            return figure
    return figure


##############################################################################################################
# Callbacks Dropdown
##############################################################################################################

@app.callback(
    Output(component_id='satellite-dropdown-component', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals')],
    [State(component_id='satellite-dropdown-component', component_property='value')]
)
def update_dropdown(clicks, value):
    global df_non_gps_h
    global df_non_gps_m
    global df_gps_h
    global df_gps_m
    global df_non_gps_h_0
    global df_non_gps_m_0
    global df_gps_h_0
    global df_gps_m_0
    global df_non_gps_h_1
    global df_non_gps_m_1
    global df_gps_h_1
    global df_gps_m_1
    global minute_data
    global minute_data_0
    global minute_data_1
    global hour_data
    global hour_data_0
    global hour_data_1
    if value == 'h45-k1':
        df_non_gps_h = df_non_gps_h_0
        df_non_gps_m = df_non_gps_m_0
        df_gps_h = df_gps_h_0
        df_gps_m = df_gps_m_0
        minute_data = minute_data_0
        hour_data = hour_data_0
    if value == 'l12-5':
        df_non_gps_h = df_non_gps_h_1
        df_non_gps_m = df_non_gps_m_1
        df_gps_h = df_gps_h_1
        df_gps_m = df_gps_m_1
        minute_data = minute_data_1
        hour_data = hour_data_1
    return value


@app.callback(
    Output(component_id='satellite-name', component_property='children'),
    [Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_satellite_name(val):
    if val == 'h45-k1':
        return 'Satellite\nH45-K1'
    elif val == 'l12-5':
        return 'Satellite\nL12-5'
    else:
        return ''


@app.callback(
    Output(component_id='satellite-description', component_property='children'),
    [Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_satellite_description(val):
    if val == 'h45-k1':
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque eget mi dictum, cursus arcu " \
               "in, porta justo. Vivamus et hendrerit sapien, sed accumsan justo. Sed sodales velit id elit egestas " \
               "aliquet. Phasellus ex tortor, ullamcorper mattis justo pulvinar, pellentesque gravida urna. Vivamus ac " \
               "libero posuere, dictum lectus at, consectetur tellus. Vestibulum non urna id ante fermentum blandit. "
        return text

    elif val == 'l12-5':
        text = "Bacon ipsum dolor amet cupim biltong rump, prosciutto filet mignon ground round flank doner. Short " \
               "ribs kielbasa pig beef. Kielbasa fatback porchetta salami, chicken bacon cow flank andouille pork " \
               "chop filet mignon t-bone. Frankfurter short ribs picanha chicken pork chop pork belly sausage, corned " \
               "beef leberkas. Shank sirloin pork spare ribs strip steak venison, chicken jowl landjaeger ham pig " \
               "prosciutto. Chuck bresaola fatback, turkey chicken pork burgdoggen andouille meatball pastrami " \
               "hamburger salami turducken. T-bone porchetta tri-tip, meatball turkey pork belly buffalo sausage " \
               "alcatra hamburger bacon cow."
        return text

    else:
        return ''


##############################################################################################################
# Callbacks Map
##############################################################################################################

@app.callback(
    Output(component_id='world-map', component_property='figure'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='control-panel-toggle-map', component_property='value'),
     Input(component_id='satellite-dropdown-component', component_property='value')],
    [State(component_id='world-map', component_property='figure')]
)
def update_word_map(clicks, toggle, satellite_type, old_figure):
    figure = old_figure
    if clicks % 2 == 0:
        figure['data'][1]['lat'] = [float(minute_data['latitude'][-1])]
        figure['data'][1]['lon'] = [float(minute_data['longitude'][-1])]

    if toggle:
        figure['data'][0]['lat'] = [df_gps_m['lat'][i] for i in range(3600)]
        figure['data'][0]['lon'] = [df_gps_m['lon'][i] for i in range(3600)]
    else:
        figure['data'][0]['lat'] = []
        figure['data'][0]['lon'] = []
    return figure


##############################################################################################################
# Callbacks Components
##############################################################################################################

@app.callback(
    Output(component_id='control-panel-utc-component', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals')],
)
def update_time(interval):
    hour = time.localtime(time.time())[3]
    if hour < 10:
        hour = '0' + str(hour)
    else:
        hour = str(hour)

    minute = time.localtime(time.time())[4]
    if minute < 10:
        minute = '0' + str(minute)
    else:
        minute = str(minute)
    return hour + ':' + minute


@app.callback(
    Output(component_id='control-panel-elevation-component', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_elevation_component(clicks, satellite_type):
    return minute_data['elevation'][-1]


@app.callback(
    Output(component_id='control-panel-temperature-component', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_temperature_component(clicks, satellite_type):
    return minute_data['temperature'][-1]


@app.callback(
    Output(component_id='control-panel-speed-component', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_speed_component(clicks, satellite_type):
    return minute_data['speed'][-1]


@app.callback(
    Output(component_id='control-panel-latitude-component', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_latitude_component(clicks, satellite_type):
    val = list(minute_data['latitude'][-1])
    if val[0] == '-':
        return '0' + ''.join(val[1::])
    return "".join(val)


@app.callback(
    Output(component_id='control-panel-longitude-component', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_longitude_component(clicks, satellite_type):
    val = list(minute_data['longitude'][-1])
    if val[0] == '-':
        return '0' + ''.join(val[1::])
    return ''.join(val)


@app.callback(
    Output(component_id='control-panel-latitude-component', component_property='color'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')],
)
def update_longitude_component(clicks, satellite_type):
    value = float(minute_data['latitude'][-1])
    if value < 0:
        return '#ff8e77'
    else:
        return '#017e84'


@app.callback(
    Output(component_id='control-panel-longitude-component', component_property='color'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')],
)
def update_longitude_component(clicks, satellite_type):
    value = float(minute_data['longitude'][-1])
    if value < 0:
        return '#ff8e77'
    else:
        return '#017e84'


@app.callback(
    Output(component_id='control-panel-fuel-component', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_fuel_component(clicks, satellite_type):
    return minute_data['fuel'][-1]


@app.callback(
    Output(component_id='control-panel-battery-component', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_battery_component(clicks, satellite_type):
    return minute_data['battery'][-1]


@app.callback(
    Output(component_id='control-panel-communication-signal', component_property='value'),
    [Input(component_id='interval', component_property='n_intervals'),
     Input(component_id='satellite-dropdown-component', component_property='value')]
)
def update_battery_component(clicks, satellite_type):
    if clicks % 2 == 0:
        return False
    else:
        return True


if __name__ == '__main__':
    app.run_server(debug=True)
