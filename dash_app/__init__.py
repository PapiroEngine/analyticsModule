from datetime import date
import dash
import dash_html_components as html
import dash_core_components as dcc
import re
import pymongo
import pandas as pd
import plotly.express as px



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

#General DB path
myclient = pymongo.MongoClient("mongodb+srv://admin:12209005@main-learninganalyticsc.kgwfb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs='CERT_NONE')
mydb = myclient["Papiro_Statistics_DB"]
mycol = mydb["Playthrough_Statistics"]

Global_Playthrough_Statistics_DF = pd.DataFrame.from_records(mycol.find())



def create_dash_app(flask_app):
    dash_app = dash.Dash(server=flask_app, name="Dashboard", url_base_pathname="/dashboardOrigin/", external_stylesheets=external_stylesheets)
    dash_app.layout = html.Div([
        dcc.DatePickerRange(
            id='my-date-picker-range',
            min_date_allowed=date(1995, 8, 5),
            max_date_allowed=date(2023, 9, 19),
            initial_visible_month=date(2021, 1, 23),
            start_date=date(2021, 1, 1),
            end_date=date(2021, 1, 25)
        ),
        html.Div(id='output-container-date-picker-range'),
        
        html.Div(
            dcc.Graph(id='chartPlayerRating'),
        )
    ])
    init_callbacks(dash_app)

    return dash_app

def init_callbacks(dash_app):
    @dash_app.callback(
        dash.dependencies.Output('chartPlayerRating', 'figure'),
        [dash.dependencies.Input('my-date-picker-range', 'start_date'),
        dash.dependencies.Input('my-date-picker-range', 'end_date')])
        
    def update_output(start_date, end_date):
        
        DF_Date_Bigger_Than_Started = Global_Playthrough_Statistics_DF[Global_Playthrough_Statistics_DF['date_started'] >= start_date]
        Final_DF = DF_Date_Bigger_Than_Started[DF_Date_Bigger_Than_Started['date_started'] <= end_date]
            
        rating_1 = len(Final_DF[Final_DF["playthrough_rating"] == 1])
        rating_2 = len(Final_DF[Final_DF["playthrough_rating"] == 2])
        rating_3 = len(Final_DF[Final_DF["playthrough_rating"] == 3])
        rating_4 = len(Final_DF[Final_DF["playthrough_rating"] == 4])
        rating_5 = len(Final_DF[Final_DF["playthrough_rating"] == 5])
        
        figRating = px.bar(y=[rating_1,rating_2,rating_3,rating_4,rating_5], x=['1 star','2 stars','3 stars','4 stars','5 stars'], title="Game Rating")
        
        return figRating
    return None
