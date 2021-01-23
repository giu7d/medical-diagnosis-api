from verify import valid_values

class Question:

	def __init__(self,name,description,dueanswer,metaanswer):
		self.name = name
		self.valid = valid_values.Valid_values()
		self.description = description
		self.valid = valid_values.Valid_values()
		self.dueanswer = dueanswer
		self.valid = valid_values.Valid_values()
		self.metaanswer = metaanswer
		self.valid = valid_values.Valid_values()

	def valid_me(self):
		acumulator = True
		x,self.Name = self.valid.is_string(self.name)
		acumulator = x and acumulator
		x,self.Description = self.valid.is_string(self.description)
		acumulator = x and acumulator
		x,self.DueAnswer = self.valid.is_date(self.dueanswer)
		acumulator = x and acumulator
		x,self.MetaAnswer = self.valid.is_json(self.metaanswer)
		acumulator = x and acumulator
		return acumulator

	def insert(self):
		if self.valid_me() :
			return self._query_add()
		else : return None

	def _query_add(self):
		def inner(tx):
			result = tx.run("create (x:Question) "
				"SET x.Name = $name "
				"SET x.Description = $description "
				"SET x.DueAnswer = $dueanswer "
				"SET x.MetaAnswer = $metaanswer "
				"return x",
				name = self.name,
				description = self.description,
				dueanswer = self.dueanswer,
				metaanswer = self.metaanswer)
			return result.single()[0]
		return inner
