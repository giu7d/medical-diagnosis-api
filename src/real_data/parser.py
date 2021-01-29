import sys

db_info = {
	"LABEL" : {} ,
	"LINK" : {} ,
}

atual_operation = {
	"OP" : None ,
	"PARAM" : None,
	"VAL" : None
}

def to_token(line):
	if line == "\n":
		return "COMMENT"
	if "->" in line:
		return "LINK"
	if "::" in line :
		return "LABEL"
	if "#" in line : 
		return "COMMENT"
	return "DATA"

def create_label(label_name,attributes):
	attributes = [ x.replace(" ","")for x in attributes]
	if not label_name in db_info["LABEL"]:
		db_info["LABEL"][label_name]={
			"PARAM" : attributes ,
			"VAL" : []
		}
		return True
	return False

def create_link(link_name,label_1,label_2,attributes):
	attributes = [ x.replace(" ","")for x in attributes]
	if not link_name in db_info["LINK"]:
		db_info["LINK"][link_name]={
			"LABEL_1" : label_1,
			"LABEL_2" : label_2,
			"PARAM" : attributes,
			"VAL" : [],
		}

def load_operation(token,value):

	if token == "COMMENT" :
		atual_operation["VAL"]=None
		return True
	
	if token == "LABEL" : 
		value = value.replace("\t"," ")
		for x in ['\n','::']: value = value.replace(x,"")
		value = " ".join(filter(lambda x:x, value.split(" ")))
		value = list(filter(lambda x: x , value.split("|")))
		label_name , *attributes = value
		label_name = label_name.replace(" ","")
		atual_operation["OP"] = token
		atual_operation["PARAM"] = label_name
		atual_operation["VAL"] = None
		create_label(label_name,attributes)
		return True
		
	if token == "DATA":
		value = value.replace('\t'," ").replace("\n","")
		value = " ".join(filter(lambda x:x, value.split(" ")))
		value = list(filter(lambda x:x,value.split("|")))
		atual_operation["VAL"] = value if value else None
		return True
		
	if token == "LINK":
		value = value.replace("\t"," ")
		for x in ['\n','->']: value = value.replace(x,"")
		value = " ".join(filter(lambda x:x, value.split(" ")))
		value = list(filter( lambda x : x , value.split("|")))
		link_name,label_1,label_2,*attributes = value
		link_name = link_name.replace(" ","")
		atual_operation["OP"] = token
		atual_operation["PARAM"] = link_name
		atual_operation["VAL"] = None
		create_link(link_name,label_1,label_2,attributes)
		return True

def generate_query_label():
	label_name = atual_operation["PARAM"]
	value = atual_operation["VAL"]
	att_name = db_info["LABEL"][label_name]["PARAM"]
	code = f'create (x:{label_name}) '
	for att,val in zip(att_name,value): 
		code += f'set x.{att} = {val} '
	code += "return x"
	return code

def generate_query_link():
	link_name = atual_operation["PARAM"]
	values = atual_operation["VAL"]
	label_1 = db_info["LINK"][link_name]["LABEL_1"].replace(" ","")
	label_2 = db_info["LINK"][link_name]["LABEL_2"].replace(" ","")
	field_1 = db_info["LABEL"][label_1]["PARAM"][0]
	field_2 = db_info["LABEL"][label_2]["PARAM"][0]
	val_1 , val_2, *att = atual_operation["VAL"]
	code = f'match (a:{label_1}) where a.{field_1} = {val_1} '
	code+= f'match (b:{label_2}) where b.{field_2} = {val_2} '
	code+= f'create (a)-[c:{link_name}]->(b) '
	attributes = db_info["LINK"][link_name]["PARAM"][:2]
	for att,val in zip(attributes,values[2:]):
		code += f'set c.{att} = {val} '
	code+= f'return c'
	return code

def generate_query():
	operation = atual_operation["OP"]
	param = atual_operation["PARAM"]
	if operation == "LABEL":
		return generate_query_label()
	if operation == "LINK" :
		return generate_query_link()
	
def apply_operation():
	if not atual_operation["VAL"] : return None
	if not atual_operation["OP"] : return None
	return generate_query()

print("match (x) detach delete x")
for line in sys.stdin:
	line = load_operation(to_token(line),line)
	query = apply_operation()
	if query : print(query)
