import neo as neo_connection
import random

neo = neo_connection.Neo4jConnection(
    uri="bolt://100.25.118.63:32789",
    user="neo4j",
    pwd="meeting-struts-pilot")

def get_year():
	while True:
		year = input("Year: ")
		try: year = int(year)
		except: continue
		if year > 2018 and year < 2022:
			return year 

def get_month():
	while True:
		mon = input("Month: ")
		try: mon = int(mon)
		except : continue
		if mon > 0 and mon < 13:
			return mon

def get_day():
	while True:
		day = input("Day: ")
		try: day = int(day)
		except: continue
		if day > 0 and day < 32:
			return day

def get_norm():
	while True:
		nrm = input("ans in interval [0,1]:")
		try: nrm = float(nrm)
		except: continue
		if nrm >= 0 and nrm <= 1:
			return nrm
		
get_str = lambda msg : f'"{input(msg)}"'
get_int = lambda msg : str(int(input(msg)))
get_dat = lambda msg : f"datetime('{get_year()}-{get_month()}-{get_day()}')"
get_jsn = lambda msg : '"'+"{'type':'range','vaxValue':110,'minValue:0'}"+'"'
get_nrm = lambda msg : get_norm()
		
structure = {
	"Disease" : {
		"SearchBy":"Name",
		"attribute" : [
			("Name","str"),
			("Description","str")
		],
		"link" : {
			"HAS" : {
				"node" : "Symptom",
				"attribute": [
					("minValue","int"),
					("maxValue","int")
				]
			},
			"REQUIRE" : {
				"node" : "Question",
				"attribute": [
					("minValue","int"),
					("maxValue","int")
				]
			}
		}
	},
	"Symptom" : {
		"SearchBy":"Name",
		"attribute" : [
			("Name","str"),
			("Description","str")
		],
		"link" : {
			"ASK" : {
				"node" : "Question",
				"attribute": []
			}
		}
	},
	"Question": {
		"SearchBy":"Name",
		"attribute" : [
			("Name","str"),
			("Description","str"),
			("DueAnswer","dat"),
			("MetaAnswer","jsn")
		],
		"link" : {},
	},
	"Person" : {
		"SearchBy":"Name",
		"attribute" : [
			("Name","str")
		],
		"link" : {
			"FEEL" : {
				"node" : "Symptom",
				"attribute": [
					("Answer","nrm"),
					("DateTime","dat")
				]
			},
			"INFO" : {
				"node" : "Question",
				"attribute": [
					("Answer","nrm"),
					("DateTime","dat")
				]
			},
			"AT" : {
				"node" : "Location",
				"attribute": [
					("DateTime","dat")
				]
			}
		}
	},
	"Location" : {
		"SearchBy":"Name",
		"attribute" : [
			("Latitude","int"),
			("Longitude","int"),
			("Name","str")
		],
		"link" : {},
	}
}

bar = lambda : print("="*60)

def data_get(msg,typ):
	while True:
		inner = {
			"str" : get_str,
			"int" : get_int,
			"jsn" : get_jsn,
			"dat" : get_dat,
			"nrm" : get_nrm,
		}
		return inner[typ](msg)
		#except : pass

def choose_option(my_list):
	while True :
		for index,element in enumerate(my_list):
			print(f"({index}) -> {element}")
		bar()
		inp = input("option: ")
		bar()
		try: return my_list[int(inp)]
		except: pass

def create(name):
	node = structure[name]
	cod = ""
	for att,typ in node["attribute"]:
		if cod : cod += ",\n\t"
		val = data_get(f"value for {name}.{att}: ",typ)
		cod += f'{att}:{val}'
	cod = f"create (:{name}"+"{"+cod+"});"
	neo.query(cod)
		
def nodes():
	return [node for node in structure]

def insert_value():
	create(choose_option(nodes()))
	
def link_value():
	node_1 = choose_option(nodes())
	val_1 = choose_option(match_all(node_1))
	link = [ i for i in structure[node_1]['link']]
	if len(link) < 1 : 
		print(f"{node_1} don't have links")
		return
	if len(link) == 1 : link = link[0]
	else : link = choose_option(link)
	
	node_2 = structure[node_1]["link"][link]["node"]
	val_2 = choose_option(match_all(node_2))
	cod = f'match (a:{node_1}'
	cod +='{'+ structure[node_1]["SearchBy"] +":"+f'"{val_1}"'+'})\n'
	cod +=f'match (b:{node_2}'
	cod +='{'+ structure[node_2]["SearchBy"] +":"+f'"{val_2}"'+'})\n'
	param = ""
	for att,typ in structure[node_1]["link"][link]["attribute"]:
		if param : param += ",\n\t"
		val = data_get(f"value for {link}.{att}: ",typ)
		param += f'{att}:{val}'
	param = '{'+param+'}'
	cod += f"create (a)-[:{link} {param}]->(b)"
	neo.query(cod)

def records_to_list(records,prop_name):
	x = []
	for record in records:
		x += [ i[prop_name] for i in record]
	return x

def match_all(name):
	cod = f"match (d:{name}) return d"
	searchBy = structure[name]["SearchBy"]
	return records_to_list(neo.query(cod),searchBy)

def show_all():
	for i in match_all(choose_option(nodes())):
		print(i)
		
def api_url_create_node(name):
	return "POST",f'api/new/{name}/'+"/".join([f'<{i[0]}>' for i in structure[name]["attribute"]])

def api_url_create_link(link_name):
	x = f"api/new/{link_name}/"
	node_1 , node_2 = "?","?"
	for node in structure:
		for i in structure[node]["link"]:
			if i == link_name : 
				node_1 = node
	node_2 = structure[node_1]["link"][link_name]["node"]
	x += f'<{node_1}_{structure[node_1]["SearchBy"]}>/'
	x += f'<{node_2}_{structure[node_2]["SearchBy"]}>/'
	temp = []
	for i,j in structure[node_1]["link"][link_name]["attribute"]:
		temp.append(f'<{i}>')
	return "POST" , x + "/".join(temp)
		
def api_url_get_node(name):
	return "GET",f'api/get/{name}/<{structure[name]["SearchBy"]}>'
		
def api_doc():
	for i in structure: print(api_url_create_node(i))
	for i in structure: 
		for j in structure[i]["link"] : 
			print(api_url_create_link(j))
	for i in structure: print(api_url_get_node(i))

def get_next_question(name):
    query = """
// doenças que a pessoa não pode ter 
// (filtro = características incompativeis)
match (person:Person { Name : """+f'"{name}"'+"""})
optional match (person)-[i:INFO]->(q:Question)<-[r:REQUIRE]-(d:Disease)
where i.DateTime + q.DueAnswer >= datetime() and
(i.Answer < r.minValue or i.Answer > r.maxValue)
with collect(d.Name) as cantHave , person , collect(r) as answered

// doenças que a pessoa pode ter
// ( todas doenças - filtro )
optional match(d:Disease)
where not d.Name in cantHave 
with person , d , answered

// questoes de caracteristicas que podem ser feitas 
//((doenças possíveis -> todas perguntas) - perguntas já realizadas )
optional match (d)-[r:REQUIRE]->(q:Question)
where not r in answered
with person , d , collect(id(q)) as infoQuestion

// sensações já respondidas
// (pessoa -> todas sensacoes informadas)
optional match(person)-[f:FELL]->(:Symptom)-[:ASK]->(q:Question)
where f.DateTime + q.DueAnswer >= datetime()
with person , d , infoQuestion ,  collect(q.Description) as answered

//questoes de sintomas que podem ser feitas
//(todas sensações - todas sensações informadas)
optional match (d)-[:HAS]->(:Symptom)-[:ASK]->(q:Question)
where not q.Description in answered

// todas questoes
// ( todas perguntas não respondidas referentes a (sensação + informação))
with person , collect(id(q)) + infoQuestion as questions

// selecionando a melhor questão
unwind questions as question
with question , count(question) as cont
match (q:Question) where id(q) = question
return q.Description as question order by cont desc limit 1
"""
    return neo.query(query)

operation = {
	"insert new node" : insert_value,
	"link new node" : link_value,
	"show all values of node" :  show_all,
	"api documentation" : api_doc,
	"exit" : "exit",
}
	
def menu():
	while True:
		op = choose_option([ i for i in operation])
		if op == "exit" : break
		operation[op]()
		bar()

#print())
menu()
