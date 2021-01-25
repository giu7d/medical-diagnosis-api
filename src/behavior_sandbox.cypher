match (p:Person) where id(p) = 25
optional match (p)-[f:FEEL]->(s:Symptom)-[a:ASK]->(q:Question)
where f.DateTime + q.DueAnswer >= datetime()
optional match (p)-[i:INFO]->(q2:Question)<-[r:REQUIRE]-(d:Disease)
where i.DateTime + q2.DueAnswer >= datetime()
optional match (s)<-[h:HAS]-(d2:Disease)
return p,f,s,a,q,q2,i,r,d,h,d2
