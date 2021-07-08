from flask import Flask, render_template, request
from dash_app import create_dash_app

app = Flask(__name__)

create_dash_app(app)

@app.route('/login')
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
