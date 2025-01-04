# figure_utils.py
import numpy as np
import plotly.graph_objs as go
import plotly.express as px

def create_trend_figure(x_values, y_values_dict, title, xaxis_title, yaxis_title,
                        show_options, category_order=None, layout_updates=None):
    """
    Creates a Plotly figure with optional bars, scatter lines, trendlines,
    and numeric labels based on the show_options checklist.
    """
    fig = go.Figure()

    # Cycle through color palette if needed
    colors = px.colors.qualitative.Plotly * (
        (len(y_values_dict) // len(px.colors.qualitative.Plotly)) + 1
    )

    for (label, y_values), color in zip(y_values_dict.items(), colors):
        show_numbers = 'numbers' in show_options
        text = y_values.apply(lambda x: f'{x:.2f}%') if show_numbers else None

        # Bar graph
        if 'bar' in show_options:
            fig.add_trace(go.Bar(
                x=x_values,
                y=y_values,
                name=label,
                marker_color=color,
                text=text,
                textposition='auto' if show_numbers else 'none',
                hovertemplate=(
                    f'<b>{label}</b><br>'
                    f'{xaxis_title}: %{{x}}<br>'
                    f'{yaxis_title}: %{{y:.2f}}%<extra></extra>'
                )
            ))

        # Scatter (distribution) plot
        if 'distribution' in show_options:
            fig.add_trace(go.Scatter(
                x=x_values,
                y=y_values,
                mode='lines+markers+text' if show_numbers else 'lines+markers',
                name=f'Scatter Plot ({label})',
                line=dict(color=color),
                marker=dict(size=8),
                text=text if show_numbers else None,
                textposition='top center',
                hovertemplate=(
                    f'<b>{label}</b><br>'
                    f'{xaxis_title}: %{{x}}<br>'
                    f'{yaxis_title}: %{{y:.2f}}%<extra></extra>'
                )
            ))

        # Trendline
        if 'trendline' in show_options:
            valid_mask = y_values.notnull() & (y_values != 0)
            if valid_mask.sum() >= 2:
                x_valid = [x for x, v in zip(x_values, valid_mask) if v]
                x_numeric = [x_values.index(x) for x in x_valid]
                y_valid = y_values[valid_mask].values
                z = np.polyfit(x_numeric, y_valid, 1)
                p = np.poly1d(z)
                trendline_y = p(x_numeric)
                fig.add_trace(go.Scatter(
                    x=x_valid,
                    y=trendline_y,
                    mode='lines',
                    name=f'Trendline ({label})',
                    line=dict(color=color, dash='dot'),
                    hoverinfo='skip'
                ))

    # Figure layout
    fig.update_layout(
        title=dict(text=title, x=0.5, xanchor='center'),
        xaxis_title=xaxis_title,
        yaxis_title=yaxis_title,
        yaxis=dict(range=[0, 100], tickformat='.2f'),
        hovermode='x unified'
    )

    if category_order:
        fig.update_xaxes(categoryorder='array', categoryarray=category_order)

    if layout_updates:
        fig.update_layout(**layout_updates)

    return fig
