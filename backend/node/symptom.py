from verify import valid_values

class Symptom:

	def __init__(self,name,description):
		self.name = name
		self.valid = valid_values.Valid_values()
		self.description = description
		self.valid = valid_values.Valid_values()

	def valid_me(self):
		acumulator = True
		x,self.Name = self.valid.is_string(self.name)
		acumulator = x and acumulator
		x,self.Description = self.valid.is_string(self.description)
		acumulator = x and acumulator
		return acumulator

	def insert(self):
		if self.valid_me() :
			return self._query_add()
		else : return None

	def _query_add(self):
		def inner(tx):
			result = tx.run("create (x:Symptom) "
				"SET x.Name = $name "
				"SET x.Description = $description "
				"return x",
				name = self.name,
				description = self.description)
			return result.single()[0]
		return inner
