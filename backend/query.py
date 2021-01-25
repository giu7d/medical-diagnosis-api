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

				"optional match (p)-[f:FEEL]->(s:Symptom)-[:ASK]->(q:Question) "
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
				" match (p:Person)"
				" where id(p) = $person_id"
				" optional match (p)-[i:INFO]->(q:Question)<-[r:REQUIRE]-(d:Disease)"
				" where i.DateTime + q.DueAnswer > datetime()"
				" and (i.Answer < r.minValue or i.Answer > r.maxValue)"
				" with p , collect(d) as incompat"
				" optional match(p)-[f:FEEL]->(s:Symptom)-[:ASK]->(q:Question)"
				" where f.DateTime + q.DueAnswer >= datetime()"
				" with p , incompat , collect(q) as answered_symptoms"
				" optional match (d:Disease)-[:HAS]->(:Symptom)-[:ASK]->(q:Question)"
				" where not d in incompat and not q in answered_symptoms"
				" with p , collect (q) as not_ans_symp , incompat"
				" optional match (p)-[i:INFO]->(q:Question)"
				" where i.DateTime + q.DueAnswer >= datetime()"
				" with p , not_ans_symp , incompat , collect(q) as answered_infos"
				" optional match (d:Disease)-[r:REQUIRE]->(q:Question)"
				" where not d in incompat and not q in answered_infos"
				" with not_ans_symp + collect(q) as questions"
				" unwind questions as question"
				" return question.Description as desc ,id(question) as quest_id , question.Name as name , question.MetaAnswer as meta , count(question) as cont order by cont DESC limit 1",
				person_id = person_id )
			return list(result)
		
		def view(record):
			return {
				"question_id" : record["quest_id"],
				"question" : record["desc"],
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
				"match (p)-[f:FEEL]->(s:Symptom) "
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
				"match (p:Person)-[f:FEEL]->(s:Symptom) "
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
