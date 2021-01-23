from verify import valid_values

class Location:

	def __init__(self,latitude,longitude,name):
		self.latitude = latitude
		self.valid = valid_values.Valid_values()
		self.longitude = longitude
		self.valid = valid_values.Valid_values()
		self.name = name
		self.valid = valid_values.Valid_values()

	def valid_me(self):
		acumulator = True
		x,self.Latitude = self.valid.is_integer(self.latitude)
		acumulator = x and acumulator
		x,self.Longitude = self.valid.is_integer(self.longitude)
		acumulator = x and acumulator
		x,self.Name = self.valid.is_string(self.name)
		acumulator = x and acumulator
		return acumulator

	def insert(self):
		if self.valid_me() :
			return self._query_add()
		else : return None

	def _query_add(self):
		def inner(tx):
			result = tx.run("create (x:Location) "
				"SET x.Latitude = $latitude "
				"SET x.Longitude = $longitude "
				"SET x.Name = $name "
				"return x",
				latitude = self.latitude,
				longitude = self.longitude,
				name = self.name)
			return result.single()[0]
		return inner
