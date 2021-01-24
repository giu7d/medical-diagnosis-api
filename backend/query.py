class Query : 

	def rank_disease(self,person_id):
		def inner(tx):
			result = tx.run(
				"match (p:Person) "
				"where id(p) = $person_id  "
				"optional match (p)-[i:INFO]->(q:Question)<-[r:REQUIRE]-(d:Disease)  "
				"where i.DateTime + q.DueAnswer >= datetime()  "
				"and (i.Answer < r.minValue or i.Answer > r.maxValue) "
				"with collect(d.Name) as cantHave , p "

				"optional match (p)-[i:INFO]->(q:Question)<-[r:REQUIRE]-(d:Disease) "
				"where i.DateTime +  duration({days:140}) >= datetime() " 
				"and i.Answer >=r.minValue  "
				"and i.Answer <= r.maxValue  "
				"and not d.Name in cantHave "
				"with p, collect(d) as diseases , cantHave "

				"optional match (p)-[f:FELL]->(s:Symptom)-[:ASK]->(q:Question) "
				"where f.DateTime + duration({days:40}) >= datetime() "
				"optional match (s)<-[h:HAS]-(d:Disease) "
				"where f.Answer <= h.maxValue  "
				"and f.Answer >= h.minValue  "
				"and not d.Name in cantHave "
				"with p, diseases + collect(d) as diseases "

				"UNWIND diseases as d "
				"return d.Name as name , count(d) as cont order by cont DESC LIMIT 3",
				person_id = person_id )
			return list(result)
		
		def view(record):
			return {
				"disease" : record["name"],
				"quantity" : record["cont"]
			}
		
		return inner , view
	
	def get_next_question(self,person_id):
		def inner(tx):
			result = tx.run(
				"match (person:Person) "
				"where id(person) = $person_id "
				"optional match (person)-[i:INFO]->(q:Question)<-[r:REQUIRE]-(d:Disease) "
				"where i.DateTime + q.DueAnswer >= datetime() and "
				"(i.Answer < r.minValue or i.Answer > r.maxValue) "
				"with collect(d.Name) as cantHave , person , collect(r) as answered "

				"optional match(d:Disease) "
				"where not d.Name in cantHave  "
				"with person , d , answered "

				"optional match (d)-[r:REQUIRE]->(q:Question) "
				"where not r in answered "
				"with person , d , collect(id(q)) as infoQuestion "

				"optional match(person)-[f:FELL]->(:Symptom)-[:ASK]->(q:Question) "
				"where f.DateTime + q.DueAnswer >= datetime() "
				"with person , d , infoQuestion ,  collect(q.Description) as answered "
				"optional match (d)-[:HAS]->(:Symptom)-[:ASK]->(q:Question) "
				"where not q.Description in answered "

				"with person , collect(id(q)) + infoQuestion as questions "

				"unwind questions as question "
				"with question , count(question) as cont "
				"match (q:Question) where id(q) = question "
				"return q.Description as question, "
				"id(q) as quest_id, "
				"q.Name as name,"
				"q.MetaAnswer as meta "
				"order by cont desc limit 1 ",
				person_id = person_id )
			return list(result)
		
		def view(record):
			return {
				"question_id" : record["quest_id"],
				"question" : record["question"],
				"name" : record["name"],
				"meta" : record["meta"]
			}
			
		return inner , view
	
	def rank_simptom_by_location(self,datetime,qt_days,radius,latitude,longitude):
		def inner(tx):
			result = tx.run(
				"with { "
				"date : datetime($datetime) , "
				"interval : duration({days:$qt_days}) , "
				"radius : $radius, "
				"latitude : $latitude , "
				"longitude : $longitude "
				"} as param "
				"match (l:Location)  "
				"where ((l.latitude - param.latitude)^2+(l.longitude - param.longitude)^2)^0.5 < param.radius "
				"match (p:Person)-[a:AT]->(l) "
				"where a.DateTime >= param.date and a.DateTime <= param.date + param.interval "
				"with p,param "
				"match (p)-[f:FELL]->(s:Symptom) "
				"where f.DateTime >= param.date and f.DateTime <= param.date + param.interval and f.Answer > 0.01 "
				"with s , count(s) as cont , avg(f.Answer) as average "
				"return s.Name as symptom, cont as quantity , average order by cont desc ",
				datetime = datetime , qt_days = qt_days , radius = radius , latitude = latitude , longitude = longitude)
			return list(result)
		
		def view(record):
			return {
				"symptom" : record["symptom"],
				"quantity" : record["quantity"]
			}
			
		return inner , view
	
	def history_symptons(self,person_id):
		def inner(tx):
			result = tx.run(
				"match (p:Person)-[f:FELL]->(s:Symptom) "
				"where f.Answer > 0.01 "
				"and id(p) = $person_id "
				"return f.DateTime as date, "
				"s.Name as symptom, "
				"f.Answer as intensity "
				"order by f.DateTime desc", 
			person_id = person_id)
			return list(result)
			
		def view(record):
			return {
				"symptom" : record["symptom"],
				"date" : 
					f'{record["date"].year}-'
					f'{record["date"].month}-'
					f'{record["date"].day}',
				"intensity":record["intensity"]
			}
		return inner , view
