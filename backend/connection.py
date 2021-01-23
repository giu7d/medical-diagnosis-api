from neo4j import GraphDatabase

class Connection:

	def __init__(self, uri, user, password):
		self.driver = GraphDatabase.driver(uri, auth=(user, password))

	def close(self):
		self.driver.close()

	def save(self, obj):
		function = obj.insert()
		if not function : return None
		with self.driver.session() as session:
			res = session.write_transaction(function)
			return res
			
	def get(self,obj_id):
		with self.driver.session() as session:
			res = session.write_transaction(self.get_by_id,obj_id)
			return res
		
	@staticmethod
	def get_by_id(tx,obj_id):
		result = tx.run("match (x)"
			" where id(x) = $obj_id return x",
			obj_id = obj_id )
		return result.single()[0]

if __name__ == "__main__" :
	from node import person
	
	c = Connection("bolt://52.72.13.205:51855","neo4j","decreases-profile-aluminum")
	p = person.Person("gooo")
	p = c.save(p)
	print(p,c.get(0))
