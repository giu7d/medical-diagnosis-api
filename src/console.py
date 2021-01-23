import neo as neo_connection
import random

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
	#return cod
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

operation = {
	"insert new node" : insert_value,
	"link new node" : link_value,
	"show all values of node" :  show_all,
	"api documentation" : api_doc,
	"exit" : "exit"
}
	
def menu():
	while True:
		op = choose_option([ i for i in operation])
		if op == "exit" : break
		operation[op]()
		bar()

valid_types = {
	"json" : 
		[
			"try: return type(eval(value)) == dict , value",
			 "except: return False , None"
		 ],
	"integer" : [" return type(value) == int , value"],
	"string" : [" return type(value) == str , value"],
	"norm" : [
		"if type(value) not in [float,int]: return False,None",
		"return (True, value) if value >= 0 and value <= 1 else (False,None)"
	],
	"date" : 
	[
		"if type(value) != str : return False,None",
		"value = value.split('-')",
		"try: int(value[0]),int(value[1]),int(value[2])",
		"except: return False,None",
		"return True,'-'.join([value[0],value[1],value[2]])"
	],
}

tab = lambda x : x * "\t"

def get_all_data_types():
	data_types = set()
	for node in nodes():
		for param,typ in structure[node]["attribute"]:
			data_types.add(typ.lower())
		for node_link in structure[node]["link"]:
			for param,typ in structure[node]["link"][node_link]["attribute"]:
				data_types.add(typ.lower())
	return data_types
	
def create_valid_value():
	
	print("class Valid_values:\n")
	data_types = get_all_data_types()
	for typ in data_types:
		print(f'{tab(1)}@staticmethod')
		print(f'{tab(1)}def is_{typ}(value):')
		cod = "\n"+tab(3)
		print(f'{tab(3)}{cod.join(valid_types[typ])}')
		print()
	
	print("import valid_values")	
	print()
	print("class Test_valid:")
	tests_ok = ['"string"',"0.1",'"1010-20-30"',"30",'\'{"a":2}\'']
	for typ in data_types:
		print(f'{tab(1)}@staticmethod')
		print(f'{tab(1)}def test_is_{typ}_from_valid():')
		print(f'{tab(2)}valid = valid_values.Valid_values()')
		print()
		for test in tests_ok:
			print(f'{tab(2)}x,y = valid.is_{typ}({test})')
			try: ns = test.replace('"','')
			except: ns = test
			print(f'{tab(2)}if x:print("{ns} is a {typ} , ret=",y)')
			print()
		print()
	print(f'if __name__ == "__main__":')
	print(f'{tab(1)}t = Test_valid()')
	for typ in data_types:
		print(f'{tab(1)}t.test_is_{typ}_from_valid()')
			
def create_model_classes():
	
	for node in nodes():
		print("from .verify import valid_values\n")
		print(f'class {node}:\n')
		cod = []
		for param,typ in structure[node]["attribute"]:
			cod.append(param.lower())
		print(f'{tab(1)}def __init__(self,{",".join(cod)}):')
		for param in cod:
			print(f'{tab(2)}self.{param} = {param}')
			print(f'{tab(2)}self.valid = valid_values.Valid_values()')
		print()
		print(f'{tab(1)}def valid_me(self):')
		print(f'{tab(2)}acumulator = True')
		for param,typ in structure[node]["attribute"]:
			print(f'{tab(2)}x,self.{param} = self.valid.is_{typ}(self.{param.lower()})')
			print(f'{tab(2)}acumulator = x and acumulator')
		print(f'{tab(2)}return acumulator')
		print()
		print(f'{tab(1)}def insert(self):')
		print(f'{tab(2)}if self.valid_me() :')
		print(f'{tab(3)}return self._query_add()')
		print(f'{tab(2)}else : return None')
		print()
		
		print(f'{tab(1)}def _query_add(self):')
		print(f'{tab(2)}def inner(tx):')
		print(f'{tab(3)}result = tx.run("create (x:{node}) "')
		cod = ""
		for att,typ in structure[node]["attribute"]:
			if cod : cod += ",\n"+tab(4)  
			cod += f'{att.lower()} = self.{att.lower()}'
		for att,typ in structure[node]["attribute"]:
			print(f'{tab(4)}"SET x.{att} = ${att.lower()} "')
		print(f'{tab(4)}"return x"{"," if cod else ""}')
		print(f'{tab(4)}{cod})')
		print(f'{tab(3)}return result.single()[0]')
		print(f'{tab(2)}return inner')
		print()

def create_api():
	for node in nodes():
		print(f'from node import {node.lower()}')
	for node in nodes():
		print()
		route = f'/v1/{node.lower()}/<int:id_{node.lower()}>'
		print(f'@app.route("{route}")')
		print(f'def get_{node.lower()}(id_{node.lower()}):')
		print()

create_api()
#create_valid_value()		
#create_model_classes()
#menu()
