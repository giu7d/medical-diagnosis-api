from flask import Flask , request
from models import *
from links import *

app = Flask(__name__)

@app.route("/v1/disease/<int:id_disease>")
def get_disease(id_disease):
	return "you try to get Disease with id "+str(id_disease)

@app.route("/v1/disease/" , methods = ["POST"])
def post_disease():
	try:
		obj = Disease().from_json(request.json)
		return "OK"
	except: print("error in POST -> Disease")
	return "fail to POST Disease with something"

@app.route("/v1/has/<int:id_disease>/<int:id_symptom>" , methods = ["POST"])
def post_has( id_disease , id_symptom ):
	obj = Link_has()
	obj.id_disease = id_disease
	obj.id_symptom = id_symptom
	obj.from_json(request.json)
	return "ok"

@app.route("/v1/require/<int:id_disease>/<int:id_question>" , methods = ["POST"])
def post_require( id_disease , id_question ):
	obj = Link_require()
	obj.id_disease = id_disease
	obj.id_question = id_question
	obj.from_json(request.json)
	return "ok"


@app.route("/v1/symptom/<int:id_symptom>")
def get_symptom(id_symptom):
	return "you try to get Symptom with id "+str(id_symptom)

@app.route("/v1/symptom/" , methods = ["POST"])
def post_symptom():
	try:
		obj = Symptom().from_json(request.json)
		return "OK"
	except: print("error in POST -> Symptom")
	return "fail to POST Symptom with something"

@app.route("/v1/ask/<int:id_symptom>/<int:id_question>" , methods = ["POST"])
def post_ask( id_symptom , id_question ):
	obj = Link_ask()
	obj.id_symptom = id_symptom
	obj.id_question = id_question
	obj.from_json(request.json)
	return "ok"


@app.route("/v1/question/<int:id_question>")
def get_question(id_question):
	return "you try to get Question with id "+str(id_question)

@app.route("/v1/question/" , methods = ["POST"])
def post_question():
	try:
		obj = Question().from_json(request.json)
		return "OK"
	except: print("error in POST -> Question")
	return "fail to POST Question with something"


@app.route("/v1/person/<int:id_person>")
def get_person(id_person):
	return "you try to get Person with id "+str(id_person)

@app.route("/v1/person/" , methods = ["POST"])
def post_person():
	try:
		obj = Person().from_json(request.json)
		return "OK"
	except: print("error in POST -> Person")
	return "fail to POST Person with something"

@app.route("/v1/feel/<int:id_person>/<int:id_symptom>" , methods = ["POST"])
def post_feel( id_person , id_symptom ):
	obj = Link_feel()
	obj.id_person = id_person
	obj.id_symptom = id_symptom
	obj.from_json(request.json)
	return "ok"

@app.route("/v1/info/<int:id_person>/<int:id_question>" , methods = ["POST"])
def post_info( id_person , id_question ):
	obj = Link_info()
	obj.id_person = id_person
	obj.id_question = id_question
	obj.from_json(request.json)
	return "ok"

@app.route("/v1/at/<int:id_person>/<int:id_location>" , methods = ["POST"])
def post_at( id_person , id_location ):
	obj = Link_at()
	obj.id_person = id_person
	obj.id_location = id_location
	obj.from_json(request.json)
	return "ok"


@app.route("/v1/location/<int:id_location>")
def get_location(id_location):
	return "you try to get Location with id "+str(id_location)

@app.route("/v1/location/" , methods = ["POST"])
def post_location():
	try:
		obj = Location().from_json(request.json)
		return "OK"
	except: print("error in POST -> Location")
	return "fail to POST Location with something"

app.run()
