import neo as neo_connection
import random

# =============================================================================
# funtion to connect on database

neo = neo_connection.Neo4jConnection(
    uri="bolt://100.26.49.182:32994",
    user="neo4j",
    pwd="logs-odds-superstructures")

import random

neo.query("match (p) detach delete p")

data = { 
    "Disease" : [],
    "Symptom" : [],
    "Question" : [],
    "Question_info" : [],
    "Person" : []
}

def str_dict(dic):
    x = []
    for k in dic:
        if dic[k] != "duration":
            v = dic[k] if not isinstance(dic[k],str) else f'"{dic[k]}"'
        else : v = rand_duration()
        x.append(f"{k}:{v}")
    x = '{'+','.join(x)+'}'
    print(x)
    return x
    
def rand_duration():
    x = { "days" : random.randint(1,5) }
    return f"duration({str_dict(x)})"

def rand_data():
    year = str(2020 - random.randint(0,1))
    month = random.randint(1,12)
    day = random.randint(1,29)
    day = str(day) if day > 9 else f"0{day}"
    month = str(month) if month > 9 else f"0{month}"
    return f'datetime("{year}-{month}-{day}")'

def rand_ans():
    return str(random.randint(0,10)/10)

def create_node(label,atributes):
    return f'create (:{label} {str_dict(atributes)})'

def disease(qt):
    for i in range(qt):
        data["Disease"].append(f"disease {i}")
        neo.query(create_node("Disease",{"Name":f"disease {i}","Description":f"descritpion of disease {i}"}))
        
def symptom(qt):
    for i in range(qt):
        data["Symptom"].append(f"symptom {i}")
        neo.query(create_node("Symptom",{"Name":f"symptom {i}","Description":f"descritpion of symptom {i}"}))

def question(qt):
    for i in range(qt):
        data["Question"].append(f"question {i}")
        neo.query(create_node("Question", {
                "Name":f"question {i}",
                "Description":f"Is this question {i}?",
                "DueAnswer":"duration",
                "MetaAnswer":"{json_example}"
            }))

def question_info(qt):
    for i in range(qt):
        data["Question_info"].append(f"question_info {i}")
        neo.query(create_node("Question", {
                "Name":f"question_info {i}",
                "Description":f"Is this question about info {i}?",
                "DueAnswer":"duration",
                "MetaAnswer":"{json_example}"
            }))
            
def person(qt):
    for i in range(qt):
        data["Person"] += [f'person {i}']
        x = 'create (:Person { Name : "person '+str(i)+'"})'
        neo.query(x)

def location():
    x = { 
            "latitude" : random.randint(0,200),
            "longitude" : random.randint(0,200)
        }
    x = f'create (:Location {str_dict(x)})'
    neo.query(x)

def has(m):
    for d in data["Disease"]:
        x = random.randint(1,m)
        s = []
        while(len(s) < x):
            rs = random.randint(0,len(data["Symptom"])-1)
            if not data["Symptom"][rs] in s :
                s.append(data["Symptom"][rs])
        for symp in s:
            cod='match (disease:Disease { Name:"'+d+'"})\n'
            cod+='match (symptom:Symptom {Name:"'+symp+'"})\n'
            y = { "minValue" : random.randint(0,5)/10 , "maxValue" : random.randint(0,5)/5 + 0.5 }
            cod+=f'create (disease)-[:HAS {str_dict(y)}]->(symptom)'
            neo.query(cod)

def require(m):
    for d in data["Disease"]:
        x = random.randint(1,m)
        s = []
        while(len(s) < x):
            rs = random.randint(0,len(data["Question_info"])-1)
            if not data["Question_info"][rs] in s :
                s.append(data["Question_info"][rs])
        for symp in s:
            cod='match (disease:Disease { Name:"'+d+'"})\n'
            cod+='match (question:Question {Name:"'+symp+'"})\n'
            y = { "minValue" : random.randint(0,100)/200 , "maxValue" : random.randint(0,100)/200 + 0.5 }
            cod+=f'create (disease)-[:REQUIRE {str_dict(y)}]->(question)'
            neo.query(cod)

def ask():
    for s,q in zip(data["Symptom"],data["Question"]):
        x = 'match (symptom:Symptom {Name:"'+s+'"})\n'
        x +='match (question:Question {Name:"'+q+'"})\n'
        x +='create (symptom)-[:ASK]->(question)'
        neo.query(x)
        
def feel(mm=9):
    for p in data["Person"]:
        qts = random.randint(1,len(data["Symptom"])-1)
        for xx in range(random.randint(1,mm)):
            s = []
            while len(s) < qts :
                ind = random.randint(1,len(data["Symptom"])-1)
                if not data["Symptom"][ind] in s : s.append(data["Symptom"][ind])
            for ss in s :
                dat = rand_data()
                x = 'match (person:Person { Name :"'+p+'"})\n'
                x+= 'match (symptom:Symptom {Name:"'+ss+'"})\n'
                x+='create (person)-[:FEEL{Answer:'+rand_ans()+',DateTime:'+dat+'}]->(symptom)'
                at(p,dat)
                neo.query(x)
                
def info(mm=9):
    for p in data["Person"]:
        qts = random.randint(1,len(data["Question_info"])-1)
        for xx in range(random.randint(1,mm)):
            s = []
            while len(s) < qts :
                ind = random.randint(1,len(data["Question_info"])-1)
                if not data["Question_info"][ind] in s : s.append(data["Question_info"][ind])
            for ss in s :
                dat = rand_data()
                x = 'match (person:Person { Name :"'+p+'"})\n'
                x+= 'match (question:Question {Name:"'+ss+'"})\n'
                x+='create (person)-[:INFO{Answer:'+rand_ans()+',DateTime:'+dat+'}]->(question)'
                at(p,dat)
                neo.query(x)

def at(p,dat):
    x,y = str(random.randint(0,200)),str(random.randint(0,200))
    
    cod='''with { x:'''+x+''' , y:'''+y+''' , p:"'''+p+'''" } as param
optional match (l:Location)
where ((l.latitude-param.x)^2+(l.longitude-param.y)^2)^0.5 < 10
call apoc.do.when(l is null,'create (ll:Location {latitude:param.x,longitude:param.y}) return ll','return l as ll',{param:param, l:l}) yield value
with param, value.ll as l, ((l.latitude-param.x)^2+(l.longitude-param.y)^2)^0.5 as distance
order by distance limit 1
match (p:Person {Name:param.p})
create (p)-[:AT {DateTime:'''+dat+'''}]->(l)'''
    neo.query(cod)
    
   
# QUANTIDADE DE DOENÇAS
disease(30)

# COLOCAR O MESMO NUMERO
symptom(60) # QT SINTOMAS
question(60) # UMA PERGUNTA PARA CADA SINTOMA

# QUANTIDADE DE PERGUNTAS PESSOAIS (IDADE, PESO, ETC)
question_info(30)

# QUANTIDADE DE PESSOAS
person(20)

# UMA DOENÇA LIGA ATÉ X SINTOMAS
has(10)

# UMA DOENÇA PRECISA DE ATÉ X CARACTERISTICAS PESSOAIS
require(10)

# CRIANDO LIGAÇÕES DO TIPO ASK
ask()

# uma pessoa respondeu algumas questões pessoais
info()

# uma pessoa sentiu algumas sintomas
feel()
