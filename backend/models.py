class Disease:

	id_disease = None
	name = None
	description = None

	def get(self):
		def inner(tx,ign):
			result = tx.run("match (x:Disease) where id(x) = $my_id return x",my_id = self.id_disease)
			return list(result)
		return inner

	def verify(self):
		if self.name == None : return False
		if self.description == None : return False
		return True

	def get_id(self):
		return self.id_disease

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run("create (x:Disease) "
				"set x.Name = $name "
				"set x.Description = $description "
				"return x", name = self.name , description = self.description)
			return list(result)
		return inner

	def from_json(self,jsn):
		try: self.name = jsn["name"]
		except: print("Name not find")
		try: self.description = jsn["description"]
		except: print("Description not find")
		return True

	def record_to_json(self,record):
		return {
			"name" : record["Name"],
			"description" : record["Description"],
			"id" : record.id
		}

class Symptom:

	id_symptom = None
	name = None
	description = None

	def get(self):
		def inner(tx,ign):
			result = tx.run("match (x:Symptom) where id(x) = $my_id return x",my_id = self.id_symptom)
			return list(result)
		return inner

	def verify(self):
		if self.name == None : return False
		if self.description == None : return False
		return True

	def get_id(self):
		return self.id_symptom

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run("create (x:Symptom) "
				"set x.Name = $name "
				"set x.Description = $description "
				"return x", name = self.name , description = self.description)
			return list(result)
		return inner

	def from_json(self,jsn):
		try: self.name = jsn["name"]
		except: print("Name not find")
		try: self.description = jsn["description"]
		except: print("Description not find")
		return True

	def record_to_json(self,record):
		return {
			"name" : record["Name"],
			"description" : record["Description"],
			"id" : record.id
		}

class Question:

	id_question = None
	name = None
	description = None
	dueanswer = None
	metaanswer = None

	def get(self):
		def inner(tx,ign):
			result = tx.run("match (x:Question) where id(x) = $my_id return x",my_id = self.id_question)
			return list(result)
		return inner

	def verify(self):
		if self.name == None : return False
		if self.description == None : return False
		if self.dueanswer == None : return False
		if self.metaanswer == None : return False
		return True

	def get_id(self):
		return self.id_question

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run("create (x:Question) "
				"set x.Name = $name "
				"set x.Description = $description "
				"set x.DueAnswer = $dueanswer "
				"set x.MetaAnswer = $metaanswer "
				"return x", name = self.name , description = self.description , dueanswer = self.dueanswer , metaanswer = self.metaanswer)
			return list(result)
		return inner

	def from_json(self,jsn):
		try: self.name = jsn["name"]
		except: print("Name not find")
		try: self.description = jsn["description"]
		except: print("Description not find")
		try: self.dueanswer = jsn["dueanswer"]
		except: print("DueAnswer not find")
		try: self.metaanswer = jsn["metaanswer"]
		except: print("MetaAnswer not find")
		return True

	def record_to_json(self,record):
		return {
			"name" : record["Name"],
			"description" : record["Description"],
			"dueanswer" : record["DueAnswer"],
			"metaanswer" : record["MetaAnswer"],
			"id" : record.id
		}

class Person:

	id_person = None
	name = None

	def get(self):
		def inner(tx,ign):
			result = tx.run("match (x:Person) where id(x) = $my_id return x",my_id = self.id_person)
			return list(result)
		return inner

	def verify(self):
		if self.name == None : return False
		return True

	def get_id(self):
		return self.id_person

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run("create (x:Person) "
				"set x.Name = $name "
				"return x", name = self.name)
			return list(result)
		return inner

	def from_json(self,jsn):
		try: self.name = jsn["name"]
		except: print("Name not find")
		return True

	def record_to_json(self,record):
		return {
			"name" : record["Name"],
			"id" : record.id
		}

class Location:

	id_location = None
	latitude = None
	longitude = None
	name = None

	def get(self):
		def inner(tx,ign):
			result = tx.run("match (x:Location) where id(x) = $my_id return x",my_id = self.id_location)
			return list(result)
		return inner

	def verify(self):
		if self.latitude == None : return False
		if self.longitude == None : return False
		if self.name == None : return False
		return True

	def get_id(self):
		return self.id_location

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run("create (x:Location) "
				"set x.Latitude = $latitude "
				"set x.Longitude = $longitude "
				"set x.Name = $name "
				"return x", latitude = self.latitude , longitude = self.longitude , name = self.name)
			return list(result)
		return inner

	def from_json(self,jsn):
		try: self.latitude = jsn["latitude"]
		except: print("Latitude not find")
		try: self.longitude = jsn["longitude"]
		except: print("Longitude not find")
		try: self.name = jsn["name"]
		except: print("Name not find")
		return True

	def record_to_json(self,record):
		return {
			"latitude" : record["Latitude"],
			"longitude" : record["Longitude"],
			"name" : record["Name"],
			"id" : record.id
		}

