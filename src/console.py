tab = lambda x : x * '\t'

structure = {
	"Disease" : {
		"SearchBy":"Name",
		"attribute" : [
			("Name","string"),
			("Description","string")
		],
		"link" : {
			"HAS" : {
				"node" : "Symptom",
				"attribute": [
					("minValue","integer"),
					("maxValue","integer")
				]
			},
			"REQUIRE" : {
				"node" : "Question",
				"attribute": [
					("minValue","integer"),
					("maxValue","integer")
				]
			}
		}
	},
	"Symptom" : {
		"SearchBy":"Name",
		"attribute" : [
			("Name","string"),
			("Description","string")
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
			("Name","string"),
			("Description","string"),
			("DueAnswer","date"),
			("MetaAnswer","json")
		],
		"link" : {},
	},
	"Person" : {
		"SearchBy":"Name",
		"attribute" : [
			("Name","string")
		],
		"link" : {
			"FEEL" : {
				"node" : "Symptom",
				"attribute": [
					("Answer","norm"),
					("DateTime","date")
				]
			},
			"INFO" : {
				"node" : "Question",
				"attribute": [
					("Answer","norm"),
					("DateTime","date")
				]
			},
			"AT" : {
				"node" : "Location",
				"attribute": [
					("DateTime","date")
				]
			}
		}
	},
	"Location" : {
		"SearchBy":"Name",
		"attribute" : [
			("Latitude","integer"),
			("Longitude","integer"),
			("Name","string")
		],
		"link" : {},
	}
}
	
def nodes():
	return [node for node in structure]
	
def links(node):
	return structure[node]['link']
	
def create_api():
	print(f'from flask import Flask , request')
	print(f'from models import *')
	print(f'from links import *')
	print(f'from connection import Connection')
	print("\napp = Flask(__name__)")
	print(f'connection = Connection("bolt://52.72.13.205:51855","neo4j","decreases-profile-aluminum")')
	for node in nodes():
		print()
		
		route = f'/v1/{node.lower()}/<int:id_{node.lower()}>'
		
		print(f'@app.route("{route}")')
		print(f'def get_{node.lower()}(id_{node.lower()}):')
		print(f'{tab(1)}obj = {node}()')
		print(f'{tab(1)}obj.id_{node.lower()} = id_{node.lower()}')
		print(f'{tab(1)}return '+'{ "values" : connection.get(obj)}')
		print()
		
		route = f'/v1/{node.lower()}/'
		print(f'@app.route("{route}" , methods = ["POST"])')
		print(f'def post_{node.lower()}():')
		print(f'{tab(1)}try:')
		print(f'{tab(2)}obj = {node}()')
		print(f'{tab(2)}obj.from_json(request.json)')
		print(f'{tab(2)}res ='+'{"values":connection.post(obj)}')
		print(f'{tab(2)}if not res : return "error to get {node}"')
		print(f'{tab(2)}else: return res')
		print(f'{tab(1)}except: print("error in POST -> {node}")')
		print(f'{tab(1)}return "fail to POST {node} with something"')
		print()
		
		for link in structure[node]['link']:
			id_1 = f'id_{node}'.lower()
			id_2 = f'id_{structure[node]["link"][link]["node"].lower()}'
			print(f'@app.route("/v1/{link.lower()}/<int:{id_1}>/<int:{id_2}>" , methods = ["POST"])')
			print(f'def post_{link.lower()}( {id_1} , {id_2} ):')
			print(f'{tab(1)}obj = Link_{link.lower()}()')
			print(f'{tab(1)}obj.{id_1} = {id_1}')
			print(f'{tab(1)}obj.{id_2} = {id_2}')
			print(f'{tab(1)}obj.from_json(request.json)')
			print(f'{tab(1)}return "ok"')
			print()
		
	print("app.run()")

def inner_get(node,ident=2):
	x = f'{tab(ident)}def inner(tx,ign):\n'
	x+= f'{tab(ident+1)}result = tx.run("match (x:{node}) where id(x) = $my_id return x",my_id = self.id_{node.lower()})\n'
	x+= f'{tab(ident+1)}return list(result)\n'
	x+= f'{tab(ident)}return inner'
	return x
	

def inner_post(node,ident=2):
	x = f'{tab(ident)}if self.verify() == False : return None\n'
	x += f'{tab(ident)}def inner(tx,ign):\n'
	x+= f'{tab(ident+1)}result = tx.run("create (x:{node}) "'
	param = []
	for y,z in structure[node]["attribute"]:
		x+= f'\n{tab(ident+2)}"set x.{y} = ${y.lower()} "'
		param.append(f'{y.lower()} = self.{y.lower()}')
	x += f'\n{tab(ident+2)}"return x", {" , ".join(param)})\n'
	x+= f'{tab(ident+1)}return list(result)\n'
	x+= f'{tab(ident)}return inner'
	return x

def create_models():
	for node in nodes():
		print(f'class {node}:\n')
		print(f'{tab(1)}id_{node.lower()} = None')
		for att,typ in structure[node]["attribute"]:
			print(f'{tab(1)}{att.lower()} = None')
		print()
		print(f'{tab(1)}def get(self):')
		print(f'{inner_get(node,2)}')
		print()
		print(f'{tab(1)}def verify(self):')
		for att,typ in structure[node]["attribute"]:
			print(f'{tab(2)}if self.{att.lower()} == None : return False')
		print(f'{tab(2)}return True')
		print()
		print(f'{tab(1)}def get_id(self):\n{tab(2)}return self.id_{node.lower()}')
		print()
		print(f'{tab(1)}def post(self):')
		print(f'{inner_post(node,2)}')
		print()
		print(f'{tab(1)}def from_json(self,jsn):')
		for att,typ in structure[node]["attribute"]:
			print(f'{tab(2)}try: self.{att.lower()} = jsn["{att.lower()}"]')
			print(f'{tab(2)}except: print("{att} not find")')
		print(f'{tab(2)}return True')
		print()
		print(f'{tab(1)}def record_to_json(self,record):')
		print(f'{tab(2)}return '+'{')
		conv = []
		for att,typ in structure[node]["attribute"]:
			conv.append(f'"{att.lower()}" : record["{att}"]')
		conv = f",\n{tab(3)}".join(conv)
		print(f'{tab(3)}{conv},')
		print(f'{tab(3)}"id" : record.id')
		print(f'{tab(2)}'+'}')
		print()

def inner_post_link(node_a,link_name,ident = 2):
	metatype = lambda typ,val : f"${val}" if typ != "date" else f'datetime(${val})'
	x  = f'{tab(ident)}def inner(tx,ign):\n'
	x += f'{tab(ident+1)}result = tx.run("'
	x += f'match (a:{node_a}) match (b:{structure[node_a]["link"][link_name]["node"]}) "\n'
	x += f'{tab(ident+2)}"where id(a) = $ida and id(b) = $idb "\n'
	x += f'{tab(ident+2)}"create (a)-[c:{link_name}]->(b) "\n'
	param = []
	for att,typ in structure[node_a]["link"][link_name]["attribute"]:
		x+= f'{tab(ident+2)}"set c.{att.lower()} = {metatype(typ,att.lower())} "\n'
		param.append(f'{att.lower()} = self.{att.lower()}')
	x+=f'{tab(ident+2)}"return c" , ida = self.id_{node_a.lower()} , idb = self.id_{structure[node_a]["link"][link_name]["node"].lower()} , {" , ".join(param)}'
	x += ')\n'
	x += f'{tab(ident+1)}return list(result)'
	return x

def create_models_links():
	for node in nodes():
		for link in links(node):
			print(f'class Link_{link.lower()}:\n')
			
			print(f'{tab(1)}id_{node.lower()} = None')
			print(f'{tab(1)}id_{structure[node]["link"][link]["node"].lower()} = None')
			for att,typ in structure[node]['link'][link]["attribute"]:
				print(f'{tab(1)}{att.lower()} = None')
			print()
			print(f'{tab(1)}def post(self):')
			print(f'{tab(2)}if self.verify() == False : return None')
			print(f'{inner_post_link(node,link)}')
			print(f'{tab(2)}return inner')
			print()
			print(f'{tab(1)}def verify(self):')
			print(f'{tab(2)}if self.id_{node.lower()} == None : return False')
			print(f'{tab(2)}if self.id_{structure[node]["link"][link]["node"].lower()} == False : return None')
			for att,typ in structure[node]['link'][link]["attribute"]:
				print(f'{tab(2)}if self.{att.lower()} == None : return False')
			print(f'{tab(2)}return True')
			print()
			print(f'{tab(1)}def from_json(self,jsn):')
			for att,typ in structure[node]['link'][link]["attribute"]:
				print(f'{tab(2)}try : self.{att.lower()} = jsn["{att.lower()}"]')
				print(f'{tab(2)}except : print("{att} not find")')
			print(f'{tab(2)}return True')
			print()
			
			
#create_models_links()
#create_models()
create_api()

