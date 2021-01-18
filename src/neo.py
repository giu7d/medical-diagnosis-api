from neo4j import GraphDatabase
import random

class Neo4jConnection:
    
    def __init__(self, uri, user, pwd):
        self.__uri = uri
        self.__user = user
        self.__pwd = pwd
        self.__driver = None
        self.models = {}
        self.nodes = {}
        self.cont = 0
        
        try:
            self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__pwd))
        except Exception as e:
            print("Failed to create the driver:", e)
        
    def close(self):
        if self.__driver is not None: self.__driver.close()
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
        
    def query(self, query, db=None):
        self.cont+= 1
        #print(f'--> {self.cont}')
        #print(query)
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try: 
            session = self.__driver.session(database=db) if db is not None else self.__driver.session() 
            response = list(session.run(query))
        except Exception as e:
            print("Query failed:", e)
        finally: 
            if session is not None:
                session.close()
        return response
        
    # define a "meta_node"
    def node(self,name):
        if not name in self.nodes:
            self.nodes[name] = []
        def inner(func):
            self.models[name] = func
            return func
        return inner
        
    def create_node_server(self,type_name,node_dict):
        cod = "create (:"+type_name+" "+self.dic_to_json(node_dict)+")"
        cod = self.query(cod)
        print(cod)
        
    # generate a random "node_name"
    def random(self,node_name):
        x = {}
        if node_name in self.models:
            model = self.models[node_name]()
            for field in model : x[field] = model[field]()
            self.create_node_server(node_name,x)
            self.nodes[node_name].append(x)
        return x
    
    # get a randomic node
    def search_random(self,node_name):
        x = {}
        if node_name in self.nodes:
            max_num = len(self.nodes[node_name])
            if max_num: 
                x = self.nodes[node_name][random.randint(0,max_num-1)]
        return x
        
    #convert a dict to json
    def dic_to_json(self,dic):
        x = ""
        for field in dic :
            if x : x += ","
            x+= field + ':'
            if type(dic[field]) == str:
                x+= f'"{dic[field]}"'
            else: x+=str(dic[field])
        return '{'+x+'}'
