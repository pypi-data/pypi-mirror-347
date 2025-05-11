import plotly.express as px
import plotly.graph_objects as go

def createLineWithHighlightChart(df, chartDefinition, colors):

    #Form figure
    fig = go.Figure()    

    #Iterate through metrics
    annotations = []
    for i in range(len(chartDefinition['metrics'])):

        #determine fill type
        if 'options' in chartDefinition:
            if 'chart-type' in chartDefinition['options']:
                if chartDefinition['options']['chart-type'] == 'area':
                    fillType = 'tozeroy'
                else:
                    fillType = 'none'
            else:
                fillType = 'none'
        else:
            fillType = 'none'

        #determine the color
        if 'options' in chartDefinition:
            if 'line-color' in chartDefinition['options']:
                lineColor = chartDefinition['options']['line-color']
            else:
                lineColor = colors[i]
        else:
            lineColor = colors[i]

        #add main line
        fig.add_trace(go.Scatter(x=df[chartDefinition['axis']],
                                    y=df[chartDefinition['metrics'][i]['name']],
                                    mode='lines',
                                    name=chartDefinition['metrics'][i]['prettyName'],
                                    line = dict(color=lineColor),
                                    fill=fillType
                                )
                        )        

        #Add the ending marker
        fig.add_trace(go.Scatter(            
            x=[df[chartDefinition['axis']][len(df)-1]],
            y=[df[chartDefinition['metrics'][i]['name']][len(df)-1]],
            mode='markers',
            marker=dict(color=lineColor, size=8)            
        ))

        #determine our text size
        if 'options' in chartDefinition:
            if 'ending-label-size' in chartDefinition['options']:
                textSize = int(chartDefinition['options']['ending-label-size'])
            else:
                textSize = 14
        else:
            textSize = 14

        #format the annotation before we add it
        rawAnnotation = df[chartDefinition['metrics'][i]['prettyColumn']][len(df)-1]
        if 'options' in chartDefinition:
            if 'ending-label-format' in chartDefinition['options']:
                if chartDefinition['options']['ending-label-format'] == 'number':
                    cleanAnnotation = f'{rawAnnotation:,}'
                elif chartDefinition['options']['ending-label-format'] == 'thousands':
                    cleanAnnotation = f'{rawAnnotation/1000:,.0f}K'
                elif chartDefinition['options']['ending-label-format'] == 'millions':
                    cleanAnnotation = f'{rawAnnotation/1000000:,.0f}M'
                elif chartDefinition['options']['ending-label-format'] == 'percent':
                    cleanAnnotation = f'{rawAnnotation:.0%}'
                elif chartDefinition['options']['ending-label-format'] == 'oneDigitNumber':
                    cleanAnnotation = f'{round(rawAnnotation, 1):,}'
                elif chartDefinition['options']['ending-label-format'] == 'twoDigitNumber':
                    cleanAnnotation = f'{round(rawAnnotation, 2):,}'
            else:
                cleanAnnotation = str(rawAnnotation)
        else:
            cleanAnnotation = str(rawAnnotation)
                

        #Add an annotation for the text itself   
        annotations.append(
            {
                'xref': 'paper', 'x': 1.003, 'y': df[chartDefinition['metrics'][i]['name']][len(df)-1],
                'xanchor': 'left', 'yanchor': 'middle', 'text': cleanAnnotation,
                'showarrow': False, 'font': {'size': textSize, 'color': lineColor}
            }
        )

    #add annotations 
    fig.update_layout(
        annotations=annotations
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


    #hide legend for now
    fig.update_layout(showlegend=False)

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

    #Force y axis to 0
    fig.update_yaxes(rangemode="tozero")

    #if we want to change the y axis type
    if 'y-axis-type' in chartDefinition:
        if chartDefinition['y-axis-type'] == 'percent':
            fig.layout.yaxis.tickformat = ',.0%'

    #return
    return fig