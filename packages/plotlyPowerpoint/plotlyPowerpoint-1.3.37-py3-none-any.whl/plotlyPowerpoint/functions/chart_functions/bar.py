import plotly.express as px
import plotly.graph_objects as go

def createBarChart(df, chartDefinition, colors, groupList):

    #add a blank colulmn to our df. this will be useful later
    df['blank'] = ''

    #if we need to sort the df
    if 'options' in chartDefinition:
        if 'sort-by' in chartDefinition['options']:
            df = df.sort_values(by=[chartDefinition['options']['sort-by']], ascending=True if chartDefinition['options']['sort-direction'] == 'ascending' else False)

    #First, define whether or not we have 1 or many metrics
    if len(chartDefinition['metrics']) == 1:
        
        #Find proper orientation of bar chart
        if 'options' in chartDefinition:
            if 'orientation' in chartDefinition['options']:
                if chartDefinition['options']['orientation'] == 'horizontal':
                    x = df[chartDefinition['metrics'][0]['name']]
                    y = df[chartDefinition['axis']]
                    orien='h'
                else:
                    x = df[chartDefinition['axis']]
                    y = df[chartDefinition['metrics'][0]['name']]
                    orien='v'
            else:
                x = df[chartDefinition['axis']]
                y = df[chartDefinition['metrics'][0]['name']]
                orien='v'
        else:
            x = df[chartDefinition['axis']]
            y = df[chartDefinition['metrics'][0]['name']]
            orien='v'

        #if we want to show data labels
        if 'options' in chartDefinition:
            if 'data-labels' in chartDefinition['options']:
                #percent
                if chartDefinition['options']['data-labels'] == 'percent':
                    df['pretty_percent'] = df[chartDefinition['metrics'][0]['name']].apply(lambda x: f'{int(round(x*100))}%')
                    textField = 'pretty_percent'
                elif chartDefinition['options']['data-labels'] == 'number':
                    df['pretty_number'] = df[chartDefinition['metrics'][0]['name']].round(0).astype(int)
                    textField = 'pretty_number'
            else:
                textField = 'blank'
        else:
            textField = 'blank'
        
        #Setup figure, based on if color is set in function
        if 'color' in chartDefinition:
            fig = px.bar(df,
                            x=x,
                            y=y,
                            color=chartDefinition['color'],
                            orientation=orien,
                            color_discrete_sequence=colors,
                            text=textField
                        )
        else:
            fig = px.bar(df,
                            x=x,
                            y=y,
                            color=groupList[0],
                            orientation=orien,
                            color_discrete_sequence=colors,
                            text=textField
                        )

    else: #multiple metrics
    
        # Create fig
        fig = go.Figure()

        # Add all bars to chart
        for i in range(len(chartDefinition['metrics'])):

            #horizontal or vertical for bar chart
            if 'options' in chartDefinition:
                if 'orientation' in chartDefinition['options']:
                    if chartDefinition['options']['orientation'] == 'horizontal':
                        x = df[chartDefinition['metrics'][i]['name']]
                        y = df[chartDefinition['axis']]
                        orien='h'
                    else:
                        x = df[chartDefinition['axis']]
                        y = df[chartDefinition['metrics'][i]['name']]
                        orien='v'
                else:
                    x = df[chartDefinition['axis']]
                    y = df[chartDefinition['metrics'][i]['name']]
                    orien='v'
            else:
                x = df[chartDefinition['axis']]
                y = df[chartDefinition['metrics'][i]['name']]
                orien='v'

            #add trace to chart    
            fig.add_trace(
                go.Bar(
                    x=x,
                    y=y,
                    name=chartDefinition['metrics'][i]['prettyName'],
                    marker_color=colors[i],
                    orientation=orien
                )
            ) 

    #change aesthetics
    fig.update_layout({
        'plot_bgcolor': 'rgba(0, 0, 0, 0)',
        'paper_bgcolor': 'rgba(0, 0, 0, 0)',
    })

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
    
    ### Handle Options
    if 'options' in chartDefinition:
        
        #If horizontal, reverse axis
        if 'orientation' in chartDefinition['options']:
            if chartDefinition['options']['orientation'] == 'horizontal':
                fig['layout']['yaxis']['autorange'] = "reversed"
        
        #If we want to hide the legend
        if 'hide-legend' in chartDefinition['options']:
            if chartDefinition['options']['hide-legend'] == True:
                fig.update_layout(showlegend=False)

        #background color
        if 'background-color' in chartDefinition['options']:
            fig.update_layout({
                'plot_bgcolor': chartDefinition['options']['background-color'],
                'paper_bgcolor': chartDefinition['options']['background-color']
            })

        #axis format
        if 'axis-format' in chartDefinition['options']:
            if 'orientation' in chartDefinition['options']:
                if chartDefinition['options']['orientation'] == 'horizontal':
                    fig.layout.xaxis.tickformat = ',.0%'
                else:
                    fig.layout.yaxis.tickformat = ',.0%'
            else:
                #do format on y axis
                if chartDefinition['options']['axis-format'] == 'percent':
                    fig.layout.yaxis.tickformat = ',.0%'




    #return
    return fig