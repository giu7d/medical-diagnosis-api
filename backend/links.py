class Link_has:

	id_disease = None
	id_symptom = None
	minvalue = None
	maxvalue = None

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run(
				"match (a:Disease) match (b:Symptom) "
				"where id(a) = $ida and id(b) = $idb "
				"create (a)-[c:HAS]->(b) "
				"set c.minvalue = $minvalue "
				"set c.maxvalue = $maxvalue "
				"return c" , 
				ida = self.id_disease , 
				idb = self.id_symptom , 
				minvalue = self.minvalue , 
				maxvalue = self.maxvalue)
			return list(result)
		return inner

	def verify(self):
		if self.id_disease == None : return False
		if self.id_symptom == False : return None
		if self.minvalue == None : return False
		if self.maxvalue == None : return False
		return True

	def from_json(self,jsn):
		try : self.minvalue = jsn["minvalue"]
		except : print("minValue not find")
		try : self.maxvalue = jsn["maxvalue"]
		except : print("maxValue not find")
		return True
		
	def record_to_json(self,record):
		return {
			"id" : record.id
		}

class Link_require:

	id_disease = None
	id_question = None
	minvalue = None
	maxvalue = None

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run(
				"match (a:Disease) match (b:Question) "
				"where id(a) = $ida and id(b) = $idb "
				"create (a)-[c:REQUIRE]->(b) "
				"set c.minvalue = $minvalue "
				"set c.maxvalue = $maxvalue "
				"return c" , 
				ida = self.id_disease , 
				idb = self.id_question , 
				minvalue = self.minvalue , 
				maxvalue = self.maxvalue)
			return list(result)
		return inner

	def verify(self):
		if self.id_disease == None : return False
		if self.id_question == False : return None
		if self.minvalue == None : return False
		if self.maxvalue == None : return False
		return True

	def from_json(self,jsn):
		try : self.minvalue = jsn["minvalue"]
		except : print("minValue not find")
		try : self.maxvalue = jsn["maxvalue"]
		except : print("maxValue not find")
		return True
		
	def record_to_json(self,record):
		return {
			"id" : record.id
		}

class Link_ask:

	id_symptom = None
	id_question = None

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run(
				"match (a:Symptom) match (b:Question) "
				"where id(a) = $ida and id(b) = $idb "
				"create (a)-[c:ASK]->(b) "
				"return c" , 
				ida = self.id_symptom , 
				idb = self.id_question )
			return list(result)
		return inner

	def verify(self):
		if self.id_symptom == None : return False
		if self.id_question == False : return None
		return True

	def from_json(self,jsn):
		return True

	def record_to_json(self,record):
		return {
			"id" : record.id
		}

class Link_feel:

	id_person = None
	id_symptom = None
	answer = None
	datetime = None

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run(
				"match (a:Person) match (b:Symptom) "
				"where id(a) = $ida and id(b) = $idb "
				"create (a)-[c:FEEL]->(b) "
				"set c.answer = $answer "
				"set c.datetime = datetime($datetime) "
				"return c" , 
				ida = self.id_person , 
				idb = self.id_symptom , 
				answer = self.answer , 
				datetime = self.datetime)
			return list(result)
		return inner

	def verify(self):
		if self.id_person == None : return False
		if self.id_symptom == False : return None
		if self.answer == None : return False
		if self.datetime == None : return False
		return True

	def from_json(self,jsn):
		try : self.answer = jsn["answer"]
		except : print("Answer not find")
		try : self.datetime = jsn["datetime"]
		except : print("DateTime not find")
		return True

	def record_to_json(self,record):
		return {
			"id" : record.id
		}

class Link_info:

	id_person = None
	id_question = None
	answer = None
	datetime = None

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run(
				"match (a:Person) match (b:Question) "
				"where id(a) = $ida and id(b) = $idb "
				"create (a)-[c:INFO]->(b) "
				"set c.answer = $answer "
				"set c.datetime = datetime($datetime) "
				"return c" , 
				ida = self.id_person , 
				idb = self.id_question , 
				answer = self.answer , 
				datetime = self.datetime)
			return list(result)
		return inner

	def verify(self):
		if self.id_person == None : return False
		if self.id_question == False : return None
		if self.answer == None : return False
		if self.datetime == None : return False
		return True

	def from_json(self,jsn):
		try : self.answer = jsn["answer"]
		except : print("Answer not find")
		try : self.datetime = jsn["datetime"]
		except : print("DateTime not find")
		return True

	def record_to_json(self,record):
		return {
			"id" : record.id
		}

class Link_at:

	id_person = None
	id_location = None
	datetime = None

	def post(self):
		if self.verify() == False : return None
		def inner(tx,ign):
			result = tx.run(
				"match (a:Person) match (b:Location) "
				"where id(a) = $ida and id(b) = $idb "
				"create (a)-[c:AT]->(b) "
				"set c.datetime = datetime($datetime) "
				"return c" , 
				ida = self.id_person , 
				idb = self.id_location , 
				datetime = self.datetime)
			return list(result)
		return inner

	def verify(self):
		if self.id_person == None : return False
		if self.id_location == False : return None
		if self.datetime == None : return False
		return True

	def from_json(self,jsn):
		try : self.datetime = jsn["datetime"]
		except : print("DateTime not find")
		return True

	def record_to_json(self,record):
		return {
			"id" : record.id
		}
