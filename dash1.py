# Import required libraries
import pandas as pd
import dash
import wget
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input,Output
import plotly.express as px 


# Read the airline data into pandas dataframe
spacex_csv_file=wget.download("https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv")
spacex_df =pd.read_csv('spacex_launch_dash.csv')

max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()
LaunchSite  = spacex_df['Launch Site'].unique()
groupLS2 = [{'label':x,'value':x} for x in sorted(LaunchSite)]
groupLS1=[{'label' : 'All site', 'value' : 'All'}]
groupLS = groupLS1 + groupLS2

# Create a dash application
app=dash.Dash(__name__)

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions=True

# Create an app layout
app.layout=html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                      style={'textAlign':'center','color':'#503D36',
                                             'font-size':40}),
                              # TASK 1: Add a dropdown list to enable Launch Site selection
                              # The default select value is for ALL sites
                              # dcc.Dropdown(id='site-dropdown',...)
                              # Create an outer division 
                              html.Div([dcc.Dropdown(id='site-dropdown',
                                                     options=groupLS,
                                                     multi = False,
                                                     placeholder='Select a Launch Site here',
                                                     searchable=True,
                                                     style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'})]),
                              html.Br(),
                              
                              # TASK 2: Add a pie chart to show the total successful launches count for all sites
                              # If a specific launch site was selected, show the Success vs. Failed counts for the site
                              html.Div(dcc.Graph(id='success-pie-chart')),
                              html.Br(),

                              html.P("Payload range (Kg):"),
                              # TASK 3: Add a slider to select payload range
                              dcc.RangeSlider(id='payload-slider',
                                              min=0,
                                              max=10000,
                                              step=1000,
                                              value=[min_payload,max_payload],
                                              marks={0:{'label':'0kg'},
                                                      2500:{'label':'2500'},
                                                      7500:{'label':'7500'},
                                                      10000:{'label':'10000'}}),

                              # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                              html.Div(dcc.Graph(id='success-payload-scatter-chart')),])
# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_graph_pie(dropdown):
    if dropdown == 'All':
        filtered_df = spacex_df[spacex_df['class']==1]
        div_data = filtered_df.groupby(['Launch Site']).size().reset_index()
        div_data=div_data.rename(columns={0:'count'})
        pie_fig = px.pie(div_data, values='count', names='Launch Site', title='Total success launches by site')
    else: 
        filtered_df = spacex_df[spacex_df['Launch Site']==dropdown]
        div_data = filtered_df.groupby(['class']).size().reset_index()
        div_data=div_data.rename(columns={0:'count'})
        pie_fig = px.pie(div_data, values='count', names='class', title='Total success launches for site '+ str(dropdown))
    return pie_fig


# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output

@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])

def get_graph_scatter(dropdown,payload):
    if dropdown == 'All':
        scatter_fig=px.scatter(spacex_df,x='Payload Mass (kg)',y='class',color="Booster Version Category",
                            title='Correlation between payload and success for all sites')
    else:
        filtered_df = spacex_df[spacex_df['Launch Site']==dropdown]
        scatter_fig=px.scatter(filtered_df,x='Payload Mass (kg)',y='class',color="Booster Version Category",
                               title='Correlation between payload and success for '+ str(dropdown))
    return scatter_fig
# Run the app
if __name__ == '__main__':
    app.run_server()