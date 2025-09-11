# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(
                                    id='site-dropdown',
                                      options=[{'label': 'All Sites', 'value': 'ALL'},
                                               {'label': 'site1', 'value': 'site1'},
                                               {'label': 'site2', 'value': 'site2'},
                                               {'label': 'site3', 'value': 'site3'},
                                               {'label': 'site4', 'value': 'site4'}]
                                      value='All',
                                      placeholder='Select a Launch Site here'
                                      searchable=True
                                      ])
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                # Function decorator to specify function input and output
                                @app.callback(Output(component_id='success-pie-chart', component_property='figure'),
                                              Input(component_id='site-dropdown', component_property='value'))
                                def get_pie_chart(entered_site):
                                    filtered_df = spacex_df
                                    if entered_site == 'ALL':
                                        fig = px.pie(data, values='class', 
                                        names='pie chart names', 
                                        title='launch success count')
                                        return fig
                                    else:
                                        filtered_df = filtered_df[filtered_df['launch_site'] == entered_site]
                                        success_counts = filtered_df['class'].value_counts()
                                        fig = px.pie(values=success_counts.values,
                                        names=success_counts.index,
                                        title=f'Success Rate for {entered_site}')
                                        return fig   
                                    # return the outcomes piechart for a selected site
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                       100: '100'},
                                                value=[min_payload, max_payload])

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                @app.callback(
                                    Output(component_id='success-payload-scatter-chart', component_property='figure'),
                                    [Input(component_id='site-dropdown', component_property='value'),
                                    Input(component_id="payload-slider", component_property="value")]
                                def update_success_payload_scatter_chart(entered_site):
                                    fig = get_scatter_chart(entered_site)
                                    return fig
                                def get_scatter_chart(entered_site):
                                    filtered_df = spacex_df
                                    if entered_site == 'All':
                                        fig = px.scatter(filtered_df, x='payload__mass_kg_', y='class', color='Booster_Version',
                                        title='Payload Mass vs Success Rate for All Sites')
                                        return fig
                                    else:
                                        filtered_df = filtered_df[filtered_df['launch_site'] == entered_site]
                                        fig = px.scatter(filtered_df, x = 'payload_mass__kg_', y='class', color='Booster_Version,')
                                        title=f'Payload Mass vs Success Rate for {entered_site}')
                                        return fig
                                # Run the app
                                if __name__ == '__main__':
                                    app.run_server()
                                    


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run()
