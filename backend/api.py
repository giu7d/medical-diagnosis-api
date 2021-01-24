from flask import Flask , request
from models import *
from query import Query
from links import *
from connection import Connection

app = Flask(__name__)

query = Query()
connection = Connection("bolt://52.72.13.205:51855","neo4j","decreases-profile-aluminum")

@app.route("/v1/disease/<int:id_disease>")
def get_disease(id_disease):
	obj = Disease()
	obj.id_disease = id_disease
	return { "values" : connection.get(obj)}

@app.route("/v1/disease" , methods = ["POST"])
def post_disease():
	try:
		obj = Disease()
		obj.from_json(request.json)
		res ={"values":connection.post(obj)}
		return res
	except: return "fail to POST Disease with something",400

@app.route("/v1/has/<int:id_disease>/<int:id_symptom>" , methods = ["POST"])
def post_has( id_disease , id_symptom ):
	obj = Link_has()
	obj.id_disease = id_disease
	obj.id_symptom = id_symptom
	obj.from_json(request.json)
	res ={"values":connection.post(obj)}
	return res

@app.route("/v1/require/<int:id_disease>/<int:id_question>" , methods = ["POST"])
def post_require( id_disease , id_question ):
	obj = Link_require()
	obj.id_disease = id_disease
	obj.id_question = id_question
	obj.from_json(request.json)
	res ={"values":connection.post(obj)}
	return res


@app.route("/v1/symptom/<int:id_symptom>")
def get_symptom(id_symptom):
	obj = Symptom()
	obj.id_symptom = id_symptom
	return { "values" : connection.get(obj)}

@app.route("/v1/symptom" , methods = ["POST"])
def post_symptom():
	try:
		obj = Symptom()
		obj.from_json(request.json)
		res ={"values":connection.post(obj)}
		return res
	except:	return "fail to POST Symptom with something",400

@app.route("/v1/ask/<int:id_symptom>/<int:id_question>" , methods = ["POST"])
def post_ask( id_symptom , id_question ):
	obj = Link_ask()
	obj.id_symptom = id_symptom
	obj.id_question = id_question
	obj.from_json(request.json)
	res ={"values":connection.post(obj)}
	return res


@app.route("/v1/question/<int:id_question>")
def get_question(id_question):
	obj = Question()
	obj.id_question = id_question
	return { "values" : connection.get(obj)}

@app.route("/v1/question" , methods = ["POST"])
def post_question():
	try:
		obj = Question()
		obj.from_json(request.json)
		res ={"values":connection.post(obj)}
		return res
	except:	return "fail to POST Question with something",400


@app.route("/v1/person/<int:id_person>")
def get_person(id_person):
	obj = Person()
	obj.id_person = id_person
	return { "values" : connection.get(obj)}

@app.route("/v1/person" , methods = ["POST"])
def post_person():
	try:
		obj = Person()
		obj.from_json(request.json)
		res ={"values":connection.post(obj)}
		return res
	except:	return "fail to POST Person with something",400

@app.route("/v1/feel/<int:id_person>/<int:id_symptom>" , methods = ["POST"])
def post_feel( id_person , id_symptom ):
	obj = Link_feel()
	obj.id_person = id_person
	obj.id_symptom = id_symptom
	obj.from_json(request.json)
	res ={"values":connection.post(obj)}
	return res

@app.route("/v1/info/<int:id_person>/<int:id_question>" , methods = ["POST"])
def post_info( id_person , id_question ):
	obj = Link_info()
	obj.id_person = id_person
	obj.id_question = id_question
	obj.from_json(request.json)
	res ={"values":connection.post(obj)}
	return res

@app.route("/v1/at/<int:id_person>/<int:id_location>" , methods = ["POST"])
def post_at( id_person , id_location ):
	obj = Link_at()
	obj.id_person = id_person
	obj.id_location = id_location
	obj.from_json(request.json)
	res ={"values":connection.post(obj)}
	return res


@app.route("/v1/location/<int:id_location>")
def get_location(id_location):
	obj = Location()
	obj.id_location = id_location
	return { "values" : connection.get(obj)}

@app.route("/v1/location" , methods = ["POST"])
def post_location():
	try:
		obj = Location()
		obj.from_json(request.json)
		res ={"values":connection.post(obj)}
		return res
	except: return "fail to POST Location with something",400

@app.route("/v1/rank_disease")
def get_rank_disease():
	person_id = int(request.args.get('person_id'))
	res = connection.query(*query.rank_disease(person_id))
	return { "value" : res }

@app.route("/v1/get_next_question")
def get_get_next_question():
	person_id = int(request.args.get('person_id'))
	res = connection.query(*query.get_next_question(person_id))
	return { "value" : res }

@app.route("/v1/rank_simptom_by_location")
def get_rank_simptom_by_location():
	datetime = request.args.get("datetime")
	qt_days = int(request.args.get("qtdays"))
	radius = float(request.args.get("radius"))
	latitude = float(request.args.get("latitude"))
	longitude = float(request.args.get("longitude"))
	res = connection.query(*query.rank_simptom_by_location(datetime,qt_days,radius,latitude,longitude))
	return { "value" : res }

@app.route("/v1/history_symptons")
def get_history_symptons():
	person_id = int(request.args.get('person_id'))
	res = connection.query(*query.history_symptons(person_id))
	return { "value" : res }

app.run()
