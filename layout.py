# layout.py
from dash import html, dcc
from data_utils import MONTHS, DAYS_OF_WEEK

def create_layout(data):
    """
    Returns the overall HTML layout for the Dash app.
    """
    return html.Div([
        html.H2('Projects Received and Not Received Trends by Time Slot'),

        # Time Aggregation Selection
        html.Div([
            html.Label('Select Time Aggregation'),
            dcc.Dropdown(
                id='time-aggregation',
                options=[
                    {'label': 'Month-Year', 'value': 'month_year'},
                    {'label': 'Month Only', 'value': 'month'},
                    {'label': 'Year Only', 'value': 'year'},
                    {'label': 'Day', 'value': 'day'}
                ],
                value='month_year'
            ),
        ], style={'width': '48%', 'display': 'inline-block'}),

        # Period Filter Selection
        html.Div([
            html.Label('Select Specific Periods'),
            dcc.Dropdown(id='period-filter', multi=True)
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

        # Days of the Week Selection
        html.Div([
            html.Label('Select Days of the Week'),
            dcc.Dropdown(
                id='day-of-week-selector',
                options=[{'label': day, 'value': day} for day in DAYS_OF_WEEK],
                multi=True,
                value=DAYS_OF_WEEK
            )
        ],
            id='day-selector-container',
            style={'width': '48%', 'display': 'inline-block', 'margin-top': '10px'}
        ),

        # Received Status Selection
        html.Div([
            html.Label('Select Received Status'),
            dcc.Dropdown(
                id='received-status-selector',
                options=[
                    {'label': 'Received', 'value': 'Received'},
                    {'label': 'Not Received', 'value': 'Not Received'},
                    {'label': 'Both', 'value': 'Both'}
                ],
                value='Both'
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block', 'margin-top': '10px'}),

        # Trend Graph Options
        html.Div([
            dcc.Checklist(
                id='trend-graph-options',
                options=[
                    {'label': 'Show Bar Graph', 'value': 'bar'},
                    {'label': 'Show Trendline', 'value': 'trendline'},
                    {'label': 'Show Scatter Plot', 'value': 'distribution'},
                    {'label': 'Show Numerical Values', 'value': 'numbers'}
                ],
                value=['bar']
            ),
        ], style={'margin-top': '10px'}),

        # Trend Graph
        dcc.Graph(id='trend-graph'),

        html.H2('Comparison of Received and Not Received Projects by Month and Year'),

        # Unified Year Selector
        html.Div([
            html.Label('Select Years'),
            dcc.Dropdown(
                id='unified-year-selector',
                options=[
                    {'label': str(year), 'value': year}
                    for year in sorted(data['year'].unique())
                ],
                multi=True,
                value=sorted(data['year'].unique())
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        # Unified Month Selector
        html.Div([
            html.Label('Select Months'),
            dcc.Dropdown(
                id='unified-month-selector',
                options=[{'label': m, 'value': m} for m in MONTHS],
                multi=True,
                value=MONTHS
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),

        # Unified Received Status
        html.Div([
            html.Label('Select Received Status'),
            dcc.Dropdown(
                id='unified-received-status-selector',
                options=[
                    {'label': 'Received', 'value': 'Received'},
                    {'label': 'Not Received', 'value': 'Not Received'},
                    {'label': 'Both', 'value': 'Both'}
                ],
                value='Both'
            )
        ], style={'width': '48%', 'display': 'inline-block', 'margin-top': '10px'}),

        # Unified Graph Options
        html.Div([
            dcc.Checklist(
                id='unified-graph-options',
                options=[
                    {'label': 'Show Bar Graph', 'value': 'bar'},
                    {'label': 'Show Trendline', 'value': 'trendline'},
                    {'label': 'Show Scatter Plot', 'value': 'distribution'},
                    {'label': 'Show Numerical Values', 'value': 'numbers'}
                ],
                value=['bar']
            ),
        ], style={'margin-top': '10px'}),

        # Unified Trend Graph
        dcc.Graph(id='unified-trend-graph'),
    ])
