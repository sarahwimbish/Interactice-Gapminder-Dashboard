# import libraries 
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output


# import the data 
data_import = pd.read_csv('gdp_pcap.csv')

# use melt to pivot the table 
data = pd.melt(data_import, id_vars=['country'], value_vars=data_import.columns[1:],var_name='year', value_name='gdp')

# convert year column to numeric 
data['year'] = pd.to_numeric(data['year'])

# convert numbers like 10K to 10000 
data['gdp'] = data['gdp'].replace({'k': '*1e3'}, regex=True).map(pd.eval).astype(int)
# code from https://stackoverflow.com/questions/39684548/convert-the-string-2-90k-to-2900-or-5-2m-to-5200000-in-pandas-dataframe

# style sheet 
stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# intialize app  
app = Dash(__name__, external_stylesheets=stylesheet) 

# data 
data = data 

# create the layout of the app 
app.layout = html.Div([

    html.H2("GDP Per Capita Across the World"), # title div 
    
    html.Div("The data that is used to build this app is from the gapminder dataset. This data set includes data about the GDP per capita of each \
             country since 1800 and estimations until 2100. To use the app, select a country-- or multiple countries-- from the dropdown menu and \
             move the slider to select a time range to look at. As you select countries they will appear on the graph and as you move the year \
             slider, the graph will adjust to only show the range selected."), # description div 

    html.Br(), # break div to make the spacing look good 

    html.Div([ # div to hold slider/dropdown 
        html.Div([ # div to hold dropdown 
            html.H4("Select Countries"), # div to hold dropdown title 
            dcc.Dropdown( # div to hold actual dropdown 
                id="country-dropdown",
                multi=True,
                options=[{"label": x, "value": x} for x in sorted(data["country"].unique())], 
                value=[sorted(data["country"].unique())[0],sorted(data["country"].unique())[1]]
        )],className="six columns"), 

        html.Div([ # div to hold slider info 
            html.H4("Select Years"), # div for slider title 
            dcc.RangeSlider( # div for actual slider 
                id ='year-slider',
                min=min(data['year']), 
                max=max(data['year']), 
                marks={i: '{}'.format(i) for i in range(min(data['year']),max(data['year']),20)}, 
                value=[min(data['year']),max(data['year'])], 
                tooltip={'always_visible': False}
            )], className= "six columns ")
    ]), 

    html.Div(dcc.Graph(id='gdp-graph'),className='twelve columns') # div that displays graph 

    ], className="row")

# add callback decorator 
@app.callback(
    Output('gdp-graph', 'figure'), # output is going to be the figure in gdp-graph
    Input('year-slider', 'value'), # get inputs from year-slider value 
    Input('country-dropdown', 'value') # get inputs from country-dropdown value 
)
def update_graph(selected_year, selected_country): # create line graph for app with title and axis labels 
    # filter the data based on the year range 
    filtered_data = data[data['year'].between(selected_year[0],selected_year[1])]
    # filter the data based on the countries selected 
    filtered_data2 = filtered_data[filtered_data['country'].isin(selected_country)]
    # actually create the figure to output 
    fig = px.line(filtered_data2, 
                x = 'year', 
                y = 'gdp',
                color = 'country',
                title = 'GPD Per Capita By Country', 
                labels={"year": "Year",
                        "gdp": "GDP Per Capita"})
    # center the title 
    fig.update_layout(title={'x':0.5,
                            'xanchor': 'center',
                            'yanchor': 'top'})
    return fig # return the figure that is based on filtered data 

# run the app 
if __name__ == '__main__':
    app.run(debug=True)