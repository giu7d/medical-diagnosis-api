from .verify import valid_values

class Person:

	def __init__(self,name):
		self.name = name
		self.valid = valid_values.Valid_values()

	def valid_me(self):
		acumulator = True
		x,self.Name = self.valid.is_string(self.name)
		acumulator = x and acumulator
		return acumulator

	def insert(self):
		if self.valid_me() :
			return self._query_add()
		else : return None

	def _query_add(self):
		def inner(tx):
			result = tx.run("create (x:Person) "
				"SET x.Name = $name "
				"return x",
				name = self.name)
			return result.single()[0]
		return inner
