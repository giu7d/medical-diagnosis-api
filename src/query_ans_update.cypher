match (p:Person) where id(p) = 25 match (q:Question) where id(q) = 321 
optional match (q)<-[:ASK]-(s:Symptom) 
with p, q , collect(id(s)) as s , 0.3 as answer , datetime() as dt
call apoc.do.when( size(s) > 0 ,
"match (s:Symptom)-[:ASK]->(q) create (p)-[f:FEEL]->(s) set x.Answer = answer set x.DateTime = dt return x ",
"create (p)-[x:INFO]->(q) set x.Answer = answer set x.DateTime = dt return x",
{p : p , q : q , answer : answer , dt : dt})
yield value 
return value.x
