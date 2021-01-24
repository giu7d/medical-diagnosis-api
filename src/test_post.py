import requests

base = lambda x : f"http://127.0.0.1:5000/v1{x}"

def test_post(url,jsn):
	print("="*60)
	print(f"request: {url}")
	res = requests.post( base(url) , json = jsn)
	print(f'status: {res.status_code}')
	print(res.json())
	#print(res)
	
def test_get(url):
	print("="*60)
	print(f"request: {url}")
	res = requests.get( base(url))
	print(f'status: {res.status_code}')
	print(res.json())

test_post("/disease",{'name': 'Name is string', 'description': 'Description is string'})

test_post("/symptom",{'name': 'Name is string', 'description': 'Description is string'})

test_post("/question",{'name': 'Name is string', 'description': 'Description is string', 'dueanswer': 'DueAnswer is date', 'metaanswer': 'MetaAnswer is json'})

test_post("/person",{'name': 'Name is string'})

test_post("/location",{'latitude': 'Latitude is integer', 'longitude': 'Longitude is integer', 'name': 'Name is string'})

test_get("/get_next_question?person_id=238")

test_get("/rank_disease?person_id=238")

test_get("/rank_simptom_by_location?datetime=2019-12-17&qtdays=100&radius=100&latitude=100&longitude=100")

test_get("/history_symptons?person_id=238")

test_post("/has/38/96",{"maxvalue":1,"minvalue":0.2})
test_post("/require/38/204",{"maxvalue":1,"minvalue":0.2})
test_post("/ask/82/120",{})
test_post("/feel/221/82",{"answer":0.5,"datetime":"2020-01-20"})
test_post("/info/221/120",{"answer":0.5,"datetime":"2020-01-20"})
test_post("/at/221/66",{"datetime":"2020-01-20"})
