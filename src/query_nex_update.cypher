match (p:Person)
where id(p) = 25

//incompativeis:
optional match (p)-[i:INFO]->(q:Question)<-[r:REQUIRE]-(d:Disease)
where i.DateTime + q.DueAnswer > datetime()
and (i.Answer < r.minValue or i.Answer > r.maxValue)
with p , collect(d) as incompat

//already answered
optional match(p)-[f:FEEL]->(s:Symptom)-[:ASK]->(q:Question)
where f.DateTime + q.DueAnswer >= datetime()
with p , incompat , collect(q) as answered_symptoms

//questions about compat diseases
optional match (d:Disease)-[:HAS]->(:Symptom)-[:ASK]->(q:Question)
where not d in incompat and not q in answered_symptoms
with p , collect (q) as not_ans_symp , incompat

//already answered infos
optional match (p)-[i:INFO]->(q:Question)
where i.DateTime + q.DueAnswer >= datetime()
with p , not_ans_symp , incompat , collect(q) as answered_infos

//questions about infos
optional match (d:Disease)-[r:REQUIRE]->(q:Question)
where not d in incompat and not q in answered_infos
with not_ans_symp + collect(q) as questions
unwind questions as question
return question , count(question) as quantity order by quantity DESC limit 1
