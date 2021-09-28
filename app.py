from flask import Flask, render_template, request, jsonify
from dash_app import create_dash_app
from flask_restful import Resource, Api
import pandas as pd
import pymongo
from json import loads
from flask_cors import CORS
import threading
from time import sleep
import redis_sub

app = Flask(__name__)
CORS(app)
api = Api(app)



create_dash_app(app)
#threading.Thread(target=redis_sub.messageReceptor).start()

#General DB path
myclient = pymongo.MongoClient("mongodb+srv://admin:12209005@main-learninganalyticsc.kgwfb.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", ssl=True,ssl_cert_reqs='CERT_NONE')
mydb = myclient["Papiro_Statistics_DB"]
mycol = mydb["Questionnaire_Templates"]

@app.route('/')
def login():
	return render_template("login.html")

#@app.route('/developer_screen')
#def developer_screen():
#	return render_template("developer_screen.html")

@app.route('/dash_presentation')
def dash_presentation():
	return render_template("dash_presentation.html")

@app.route('/questionnaireCreation')
def form():
	return render_template("form.html")

@app.route('/thankyou', methods=["POST"])
def thankyou():
    clicks = request.form.get("ClickCounter")
    senha = request.form.get("clicks")
    questTitle = request.form.get("questname")
    jsonString = "{\"questions\":["
    for click in range(int(clicks)):
        question = request.form.get("textBox_Question_" + str(click+1))
        altA = request.form.get("AlternativeA_Question_" + str(click+1))
        altB = request.form.get("AlternativeB_Question_" + str(click+1))
        altC = request.form.get("AlternativeC_Question_" + str(click+1))
        altD = request.form.get("AlternativeD_Question_" + str(click+1))
        if(not altA): #Checa se altA está em vazio para decidir se é questão de escala ou alternativa
            info = {
            "questionNumber": str(click+1),
            "questionText": question,
            "type": "Scale"
            }
            jsonString += ("{\"question\":\"" + question + "\",\"type\":\"Scale\"},")
        else:
            info = {
            "questionNumber": str(click+1),
            "questionText": question,
            "type": "Alternative",
            "alternatives": [altA,altB,altC,altD],
            }
            jsonString += ("{\"question\":\"" + question + ":\",\"type\":\"Alternative\",\"alternatives\":[{\"alternative\":\"" + altA + "\"},{\"alternative\":\"" + altB + "\"},{\"alternative\":\"" + altC + "\"},{\"alternative\":\"" + altD + "\"}]},")
    jsonString = jsonString[:-1]
    jsonString += "],\"questionnaireTitle\":\"" + questTitle + "\",\"Creator_Id\":\"" + "TestePlataforma" + "\"}"


    print(jsonString)
    data = loads(jsonString)
    mycol.insert_one(data)
    return render_template("thankyou.html", email=jsonString, senha=senha)




auth_token = "LDhkmZP2tkXBTmrB4TNjKQQtXftJBJT337YZVumerK4ensx6Z4afxLy3kuQPJZGFEqW7jnLNYJFYKefbWUhp24MtzGa5T2fDg3Nvnp3DfPXhc27cW7kXZQ3SpJ2XGMxv"

class Teste(Resource):
    def get(self, creatorID, auth):
        if auth != auth_token:
            return False
        else:
            a = mycol.find({"$or":[{"Creator_Id":creatorID}, {"Creator_Id":"Template"}]},{"_id": 0})
            b = jsonify(list(a))
            return b

api.add_resource(Teste, '/questionnaires/templates/<creatorID>/<auth>')