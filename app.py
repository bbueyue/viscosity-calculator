import numpy as np

import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State


# Initialise the app
app = dash.Dash(__name__)

server = app.server

# Design the dashboard
app.layout = html.Div(children=[
                  html.Div(className='row',  # Define the row element
                           children=[
                           # Add the logo
                           html.Img(src="assets/logo.svg",  width=400, style={'display' : 'inline-block'}),
                           html.Div(style={'text-align':'center', },
                                    children = [
                                        # App title
                                        html.P('RT-DC Buffers Viscosity Calculator', style = {'font-size': '25px', 'text-align':'center'}),
                                        html.Br(),
                                        # Dropdown menu division (titile and design)
                                        html.Div([
                                              html.H2('Medium', style = {'font-size': '14px'}),
                                              dcc.Dropdown(id="medium",
                                                           options=[
                                                                   {'label': '0.5% MC-PBS', 'value': 'M1'},
                                                                   {'label': '0.6% MC-PBS', 'value': 'M2'},
                                                                   {'label': '0.84% MC-PBS', 'value': 'M3'}
                                                                    ],
                                                           searchable=True,
                                                           placeholder='Select a medium',
                                                           style={'width': '250px', 
                                                                  'color': 'blue',
                                                                  'display' : 'inline-block'}
                                                          )]),
                                        # Temparature input box division (titile and design)    
                                        html.Div([
                                              html.H2('Temperature [°C]', style = {'font-size': '14px'}),
                                              dcc.Input(id="temperature",
                                                        placeholder='Enter the temperature...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '250px'}
                                                       )]),
                                        # Channel size input box division (titile and design)
                                        html.Div([
                                              html.H2('Channel size [μm]', style = {'font-size': '14px'}),
                                              dcc.Input(id="channel_size",
                                                        placeholder='Enter the channel size...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '250px'}
                                                       )]),
                                        # Flowrate input box division (titile and design)    
                                        html.Div([
                                              html.H2('Flowrate [μl/s]', style = {'font-size': '14px'}),
                                              dcc.Input(id="flowrate",
                                                        placeholder='Enter the flowrate...',
                                                        type='text',
                                                        persistence = False,
                                                        style={'width': '250px'}
                                                       )]),
                                        html.Br(), 
                                        # Store component for input storage
                                        dcc.Store(id = 'store_viscosity'),
                                        # Submit button design 
                                        html.Button('Submit', id='submit_button', n_clicks=0, disabled=False, 
                                                    style = {'font-size': '12px',
                                                              'cursor': 'pointer',
                                                              'text-align': 'center',
                                                              'color': 'white',
                                                            }
                                                    ),
                                        html.Br(), html.Br(), 
                                        # Output component to display viscosity value
                                        html.Div(id='show_viscosity', style={'whiteSpace': 'pre-line', 
                                                                                'font-size': '20px'})
                                        
                                  ]),  
                          ]) # row Div
                    ]) # main Div

# This callback function takes the inputs from
# the html components (see the id's), compute 
# the viscosity and store it in dcc.Store 
# component as key and value pair
@app.callback(
    Output("store_viscosity", "data"),
   [Input("medium", "value"),
    Input("temperature", "value"),
    Input("channel_size", "value"),
    Input("flowrate", "value")])

def compute_viscosity(medium, temperature, channel_size, flow_rate):
    features_str = [temperature, channel_size, flow_rate]
    if len(features_str) == 3 and None not in features_str and '' not in features_str:

        if medium=='M1':
            n_MC05 = 0.0026*float(temperature) + 0.590
            K_MC05 = 0.05*np.exp(35*(1/float(temperature)))
            shear_rate_05 = 8*float(flow_rate)/((float(channel_size)*1e-3)**3)*(0.6671+0.2121/n_MC05)
            viscosity = K_MC05*shear_rate_05**(n_MC05-1)*1000
            viscosity = np.round(viscosity,2)
            return {'viscosity' : viscosity}

        if medium=='M2':
            n_MC06 = 0.0024*float(temperature) + 0.529
            K_MC06 = 0.15*np.exp(27.8*(1/float(temperature)))
            shear_rate_06 = 8*float(flow_rate)/((float(channel_size)*1e-3)**3)*(0.6671+0.2121/n_MC06)
            viscosity = K_MC06*shear_rate_06**(n_MC06-1)*1000#
            viscosity = np.round(viscosity,2)
            return {'viscosity' : viscosity}

        if medium=='M3':
            n_MC084 = 0.0021*float(temperature) + 0.467
            K_MC084 = 0.40*np.exp(30.6*(1/float(temperature)))
            shear_rate_084 = 8*float(flow_rate)/((float(channel_size)*1e-3)**3)*(0.6671+0.2121/n_MC084)
            viscosity = K_MC084*shear_rate_084**(n_MC084-1)*1000
            viscosity = np.round(viscosity, 2)
            return {'viscosity' : viscosity}

  
# This call back function is activated when 
# user click on submit button. When do so, stored
# viscosity value will be diyplayed in the output 
# component
@app.callback(
    Output('show_viscosity', 'children'),
    Input('submit_button', 'n_clicks'),
    State('store_viscosity', 'data'))

def display_output(n_clicks, stored_viscosity):
    trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if stored_viscosity is not None:
        viscosity = stored_viscosity['viscosity']
        if 'submit_button' in trigger:
            return 'Computed viscosity [mPa.s]: \n{}'.format(viscosity)
        else:
            return dash.no_update
    else:
        return dash.no_update
    

# This call back function will reset the input boxes
# as soon as user click on the submit button
@app.callback(
   [Output("temperature", "value"),
    Output("channel_size", "value"),
    Output("flowrate", "value")], 
     Input('submit_button', 'n_clicks'))

def reset_inputs(click):
    trigger = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit_button' in trigger:
        return ['']*3
    else:
        return dash.no_update


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False)




