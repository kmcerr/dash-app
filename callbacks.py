# callbacks.py
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

from data_utils import DAYS_OF_WEEK, MONTHS, calculate_percentages
from figure_utils import create_trend_figure

def register_callbacks(app, data):
    """
    Register all Dash callbacks. This function is called from main.py.
    """

    @app.callback(
        [Output('period-filter', 'options'), Output('period-filter', 'value')],
        [Input('time-aggregation', 'value')]
    )
    def update_period_filter(aggregation_type):
        if aggregation_type == 'month_year':
            options = [{'label': i, 'value': i} for i in sorted(data['month_year'].unique())]
        elif aggregation_type == 'year':
            options = [{'label': str(i), 'value': i} for i in sorted(data['year'].unique())]
        elif aggregation_type == 'month':
            # Keep the proper month order using .cat.categories if needed
            options = [{'label': i, 'value': i} for i in data['month'].cat.categories]
        elif aggregation_type == 'day':
            options = [{'label': i, 'value': i} for i in DAYS_OF_WEEK]
        else:
            options = []

        value = [options[-1]['value']] if options else []
        return options, value

    @app.callback(
        Output('day-selector-container', 'style'),
        [Input('time-aggregation', 'value')]
    )
    def update_day_selector_visibility(aggregation_type):
        if aggregation_type == 'day':
            return {'display': 'none'}
        else:
            return {'width': '48%', 'display': 'inline-block', 'margin-top': '10px'}

    @app.callback(
        Output('trend-graph', 'figure'),
        [
            Input('time-aggregation', 'value'),
            Input('period-filter', 'value'),
            Input('day-of-week-selector', 'value'),
            Input('received-status-selector', 'value'),
            Input('trend-graph-options', 'value')
        ]
    )
    def update_trend_graph(agg_type, selected_periods, selected_days, received_status, show_options):
        if not selected_periods:
            return go.Figure()

        time_slots = [
            '08:30', '09:00', '09:30', '10:00', '10:30',
            '11:00', '11:30', '12:00', '12:30', '13:00',
            '13:30', '14:00', '14:30', '15:00', '15:30'
        ]
        x_values = time_slots
        y_values_dict = {}

        statuses = ['Received', 'Not Received'] if received_status == 'Both' else [received_status]

        for period in selected_periods:
            if agg_type == 'month_year':
                filtered_data = data[data['month_year'] == period]
                label_prefix = str(period)
            elif agg_type == 'year':
                filtered_data = data[data['year'] == int(period)]
                label_prefix = str(period)
            elif agg_type == 'month':
                filtered_data = data[data['month'] == period]
                label_prefix = str(period)
            elif agg_type == 'day':
                filtered_data = data[data['day'] == period]
                label_prefix = str(period)
            else:
                filtered_data = data.copy()
                label_prefix = 'All Data'

            if filtered_data.empty:
                continue

            if agg_type != 'day' and selected_days:
                filtered_data = filtered_data[filtered_data['day'].isin(selected_days)]

            trend_data = filtered_data.groupby(['time', 'received']).size().unstack(fill_value=0)
            trend_data_percent = calculate_percentages(trend_data).reindex(time_slots, fill_value=0)

            for status in statuses:
                y_values = trend_data_percent.get(status, pd.Series(0, index=time_slots))
                label = f'{label_prefix} - {status}'
                y_values_dict[label] = y_values

        title = (
            f"Distribution of Projects by Time Slot<br>"
            f"Selected {agg_type.capitalize()}: {', '.join(map(str, selected_periods))}"
        )
        if agg_type != 'day' and selected_days:
            title += f"<br>Selected Days: {', '.join(selected_days)}"

        fig = create_trend_figure(
            x_values,
            y_values_dict,
            title,
            'Time Slot',
            'Percentage',
            show_options,
            category_order=time_slots
        )
        return fig

    @app.callback(
        Output('unified-trend-graph', 'figure'),
        [
            Input('unified-year-selector', 'value'),
            Input('unified-month-selector', 'value'),
            Input('unified-received-status-selector', 'value'),
            Input('unified-graph-options', 'value')
        ]
    )
    def update_unified_trend_graph(selected_years, selected_months, received_status, show_options):
        if not selected_years or not selected_months:
            return go.Figure()

        x_values = MONTHS
        y_values_dict = {}
        statuses = ['Received', 'Not Received'] if received_status == 'Both' else [received_status]

        for year in selected_years:
            for status in statuses:
                filtered_data = data[
                    (data['year'] == year) &
                    (data['month'].isin(selected_months)) &
                    (data['received'] == status)
                ]
                if filtered_data.empty:
                    continue

                trend_data = (
                    filtered_data.groupby('month', observed=False)
                    .size()
                    .reindex(MONTHS, fill_value=0)
                )
                total_projects = (
                    data[
                        (data['year'] == year) &
                        (data['month'].isin(selected_months))
                    ]
                    .groupby('month', observed=False)
                    .size()
                    .reindex(MONTHS, fill_value=0)
                )

                y_values = (trend_data / total_projects) * 100
                y_values = y_values.fillna(0).round(2)

                label = f'{year} - {status}'
                y_values_dict[label] = y_values

        title = (
            f"Comparison of Projects by Month and Year<br>"
            f"Selected Years: {', '.join(map(str, selected_years))}<br>"
            f"Selected Months: {', '.join(selected_months)}"
        )
        fig = create_trend_figure(
            x_values,
            y_values_dict,
            title,
            'Month',
            'Percentage',
            show_options,
            category_order=MONTHS,
            layout_updates={'barmode': 'group'}
        )
        return fig
