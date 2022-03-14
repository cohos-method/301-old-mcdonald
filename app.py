import dash
from dash import Dash, dcc, html
from dash import html as html
from dash.dependencies import Input, Output, State
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import numpy as np
import math
import datetime as dt

########### Define your variables ######

# here's the list of possible columns to choose from.
file_idx = "assets/index.csv"
file_demo = "assets/demographics.csv"
#file_geo = "assets/geography.csv"
#file_hosp = "assets/hospitalizations.csv"


mycolumn='population'
myheading1 = f"Wow! That's a lot of people!"

tabtitle = 'Cohos-Method - Population by Country'
sourceurl = 'https://plot.ly/python/choropleth-maps/'



#lambdas & functions
get_me_dataframe = lambda f : pd.read_csv(f)

formatlisttext = lambda l: [ s.replace("_", " ").replace("population", "").replace("age", "age between").strip().title() for s in l]

def drawPlot(selectedColumn, dataframe, locations, color, hover_name):

    mycolumn_title = selectedColumn.replace ("_", " ")
    mycolumn_title = mycolumn_title.title()
    mygraphtitle = f'{mycolumn_title} By Country'
    mycolorscale = 'ylorrd' # Note: The error message will list possible color scales.
    mycolorbartitle = f"Millions of {mycolumn_title}"

    # sorting
    dataframe.sort_values(by=selectedColumn, ascending=False, inplace=True)

    df_x = dataframe[:25]
    #df_x['bubblesize'] = (df_x[selectedColumn]/1000000).astype(int)
    #df_x['hovertext'] = df['country_name'  + " " + title + " " + df['size']]

    fig = px.scatter_geo(df_x
                         , locations="iso_3166_1_alpha_3"
                         , color=selectedColumn
                         , hover_name="country_name"
                         , size=selectedColumn)
    #selectedColumn)

    fig.update_geos(projection_type="natural earth")

    fig.update_layout(
        title_text = mygraphtitle,
        width=900,
        height=600)
    return fig



## List of Options prep
strlist = "population,population_male,population_female,population_rural,population_urban,population_largest_city,population_clustered,population_density,population_age_00_09,population_age_10_19,population_age_20_29,population_age_30_39,population_age_40_49,population_age_50_59,population_age_60_69,population_age_70_79,population_age_80_and_older"
list_of_options = strlist.split(sep=",")

#print (list_of_options)
formatlisttext = lambda l: [ s.replace("_", " ").replace("population", "").replace("age", "age between").strip().title() for s in l]
list_of_options_text = formatlisttext(list_of_options)
list_of_options_text[0] = "All Population"
#print(list_of_options_text)

choices = []
for i in range(len(list_of_options)):
    d = {'label':list_of_options_text[i], 'value':list_of_options[i]}
    choices.append(d)

########## Set up the chart

# loading up the data frames and merging them
df_idx = get_me_dataframe(file_idx)
df_demo = get_me_dataframe(file_demo)
#df_geo = get_me_dataframe(file_geo)

#... and merging them
df_m = pd.merge(df_idx, df_demo, how="inner", on="location_key")
#df_m = pd.merge(df_m, df_geo, how="inner", on="location_key")

df_m.drop(columns=['wikidata_id'
                   , 'datacommons_id'
                   , 'subregion1_code'
                   , 'subregion1_name'
                   , 'subregion2_code'
                   , 'subregion2_name'
                   , 'locality_code'
                   , 'locality_name'
                   , 'aggregation_level']
         , axis=1
         , inplace=True)

df_m.sort_values(by=mycolumn
                 , ascending=False
                 ,inplace=True)

# data cleanup
cols = "population,population_male,population_female,population_rural,population_urban,population_largest_city,population_clustered,population_density,human_development_index,population_age_00_09,population_age_10_19,population_age_20_29,population_age_30_39,population_age_40_49,population_age_50_59,population_age_60_69,population_age_70_79,population_age_80_and_older"

clist = cols.split(sep=',')

for c in clist:
    print (c)
    df_m[c] = df_m[c].fillna(0)
    df_m[c] = df_m[c].astype(int)

# prepare the params and call the function  to draw the plot
dataframe = df_m
locations = "iso_3166_1_alpha_3"
color = mycolumn
hover_name = "country_name"

fig  = drawPlot(mycolumn, dataframe, locations, color, hover_name)


########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Set up the layout
app.layout = html.Div(children=[
    html.H1(myheading1),
    html.H4("Pick your choice for population"),
    dcc.Dropdown(
        id='your_input_here',
        options = choices,
        value="population",
        ),
    html.Div(id='your_output_here', children=''),
    dcc.Graph(id='figure-1', figure=fig
    )#,

    #html.A('Code on Github', href=githublink),
    #html.Br(),
    #html.A("Data Source", href=sourceurl),
    ]
)

########## Define Callback
@app.callback(Output('figure-1', 'figure'),
              [Input('your_input_here', 'value')])
def radio_results(myselection):
    print ("********  myselection: ", myselection)
    #preparing the parameters
    dataframe = df_m
    locations = "iso_3166_1_alpha_3"
    color = myselection
    hover_name = "country_name"
    size = myselection
    fig = drawPlot(myselection, dataframe, locations, color, hover_name)
    print ("********  fig: ", fig)

    return fig


############ Deploy
if __name__ == '__main__':
    app.run_server()
