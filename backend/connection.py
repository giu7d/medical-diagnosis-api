from neo4j import GraphDatabase

class Connection:

	def __init__(self, uri, user, password):
		self.driver = GraphDatabase.driver(uri, auth=(user, password))

	def close(self):
		self.driver.close()

	def post(self, obj):
		if None == obj.post(): return None
		with self.driver.session() as session:
			res = session.write_transaction(obj.post(),None)
			return res
			
	def get(self,obj):
		if None == obj.get_id() : return None
		with self.driver.session() as session:
			res = session.write_transaction(obj.get(),None)
			return [obj.record_to_json(i) for i in res[0]]
		
	

if __name__ == "__main__" :
	from models import Person
	from links import *
	
	c = Connection("bolt://52.72.13.205:51855","neo4j","decreases-profile-aluminum")
	#l = Link_info()
	#l.id_person = 0
	#l.id_question = 2488
	#l.answer = 1
	#l.datetime="2030-10-10"
	p = Person()
	p.id_person = 0
	#p.name = "lar"
	print(c.get(p))
