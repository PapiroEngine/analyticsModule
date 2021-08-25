from flask import Flask, render_template, request
from dash_app import create_dash_app
from flask_restful import Resource, Api
import pandas as pd
import pymongo
from bson.json_util import dumps

app = Flask(__name__)
api = Api(app)

create_dash_app(app)

@app.route('/')
def login():
	return render_template("login.html")

@app.route('/developer_screen')
def developer_screen():
	return render_template("developer_screen.html")

@app.route('/dash_presentation')
def dash_presentation():
	return render_template("dash_presentation.html")

@app.route('/form')
def form():
	return render_template("form.html")

@app.route('/thankyou', methods=["POST"])
def thankyou():
	email = request.form.get("testeemail")
	senha = request.form.get("senha")
	return render_template("thankyou.html", email=email, senha=senha)


#General DB path
myclient = pymongo.MongoClient("mongodb+srv://admin:12209005@main-learninganalyticsc.kgwfb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs='CERT_NONE')
mydb = myclient["Papiro_Statistics_DB"]
mycol = mydb["Questionnaire_Templates"]

auth_token = "LDhkmZP2tkXBTmrB4TNjKQQtXftJBJT337YZVumerK4ensx6Z4afxLy3kuQPJZGFEqW7jnLNYJFYKefbWUhp24MtzGa5T2fDg3Nvnp3DfPXhc27cW7kXZQ3SpJ2XGMxv"

class Teste(Resource):
    def get(self, questType, auth):
        if auth != auth_token:
            return False
        else:
            a = mycol.find({"CreatorID": questType },{"_id": 0})
            b = list(a)
            return dumps(b)

api.add_resource(Teste, '/questionnaires/templates/<questType>/<auth>')