import plotly.express as px
import plotly.graph_objects as go

def createFilledLineChart(df, chartDefinition, colors):

    #Figure out if there are multiple metrics. If so, throw an error
    if len(chartDefinition['metrics']) == 1:

        #Determine if we're grouping by color or not
        if 'color' in chartDefinition:  
            fig = px.area(df,
                            x=chartDefinition['axis'],
                            y=chartDefinition['metrics'][0]['name'],
                            color_discrete_sequence= colors,
                            color=chartDefinition['color'])
        else:
            fig = px.area(df,
                        x=chartDefinition['axis'],
                        y=chartDefinition['metrics'][0]['name'],
                        color_discrete_sequence=colors
                            )

    else: #we have multiple metrics 

        raise ValueError('Filled line charts can only have one metric. Please convert your metrics into a variable:value format and break out the line chart by color')


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
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        xanchor="center",
        x=.5,
        y=-.3,
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

    #return
    return fig