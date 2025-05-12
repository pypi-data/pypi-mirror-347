import plotly.express as px
import plotly.graph_objects as go

def createLineChart(df, chartDefinition, colors):

    #first, figure out if we have multiple metrics. Chart is very different if multiple
    if len(chartDefinition['metrics']) == 1:                

        #Determine if we're grouping by color or not
        if 'color' in chartDefinition:  
            fig = px.line(df,
                            x=chartDefinition['axis'],
                            y=chartDefinition['metrics'][0]['name'],
                            color_discrete_sequence= colors,
                            color=chartDefinition['color'])
        else:
            fig = px.line(df,
                        x=chartDefinition['axis'],
                        y=chartDefinition['metrics'][0]['name'],
                        color_discrete_sequence=colors
                            )

    else: #we have multiple metrics 

        # Create fig
        fig = go.Figure()

        # Add all lines to the chart
        for i in range(len(chartDefinition['metrics'])):
            fig.add_trace(go.Scatter(x=df[chartDefinition['axis']],
                                        y=df[chartDefinition['metrics'][i]['name']],
                                        mode='lines',
                                        name=chartDefinition['metrics'][i]['prettyName'],
                                        line = dict(color=colors[i])
                                    )
                            )

    #change aesthetics
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

    ### Handle all options
    if 'options' in chartDefinition:

        ### Grid lines
        if 'horizontal-grid-lines' in chartDefinition['options']:
            if chartDefinition['options']['horizontal-grid-lines'] == 'true':
                fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#ebebeb')

        if 'vertical-grid-lines' in chartDefinition['options']:
            if chartDefinition['options']['vertical-grid-lines'] == 'true':
                fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#ebebeb', title="")

        ### X axis ticks rotation
        if 'x-axis-ticks-angle' in chartDefinition['options']:
            fig.update_xaxes(nticks=df[chartDefinition['axis']].nunique(), tickangle=chartDefinition['options']['x-axis-ticks-angle'])

        ### Background color
        if 'background-color' in chartDefinition['options']:
            fig.update_layout({
                'plot_bgcolor': chartDefinition['options']['background-color'],
                'paper_bgcolor': chartDefinition['options']['background-color']
            })

        ## Text Size - X Axis
        if 'x-axis-text-size' in chartDefinition['options']:
            fig.update_layout( xaxis = dict( tickfont = dict(size=int(chartDefinition['options']['x-axis-text-size']))))

        ## Text Size - Y Axis
        if 'y-axis-text-size' in chartDefinition['options']:
            fig.update_layout( yaxis = dict( tickfont = dict(size=int(chartDefinition['options']['y-axis-text-size']))))


    #update legend
    lengend_position_x = 0.5
    legend_position_y = -0.3
    if 'options' in chartDefinition:
        if 'legend-position-x' in chartDefinition['options']:
            lengend_position_x = chartDefinition['options']['legend-position-x']

        if 'legend-position-y' in chartDefinition['options']:
            lengend_position_y = chartDefinition['options']['legend-position-y']            

    fig.update_layout(legend=dict(
        orientation="h",
        yanchor='bottom',
        xanchor="center",
        x=lengend_position_x,
        y=-legend_position_y,
        title=""
    ))

    #X axis title
    if 'x-axis-title' in chartDefinition:
        fig.update_layout(
            xaxis_title=chartDefinition['x-axis-title']
        )

    #Y axis title
    if 'y-axis-title' in chartDefinition:
        fig.update_layout(
            yaxis_title=chartDefinition['y-axis-title']
        )
    
    #if we want to change the y axis type
    if 'y-axis-type' in chartDefinition:
        if chartDefinition['y-axis-type'] == 'percent':
            fig.layout.yaxis.tickformat = ',.0%'

    #return
    return fig