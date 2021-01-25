import requests

base = lambda x : f"http://127.0.0.1:5000/v1{x}"

def test_post(url,jsn):
	print("="*60)
	print(f"request: {url}")
	res = requests.post( base(url) , json = jsn)
	print(f'status: {res.status_code}')
	print(res.json())
	return res.json()
	#print(res)
	
def test_get(url):
	print("="*60)
	print(f"request: {url}")
	res = requests.get( base(url))
	print(f'status: {res.status_code}')
	print(res.json())
	return res.json()


def tests():

	'test : criating a person'
	x = test_post("/person",{"name":"PERSON TESTE"})
	person_id = x['values'][0]['id']


	'test : creating a disease'
	x = test_post("/disease",{'name': 'DISEASE TEST', 'description': 'Description is string'})
	disease_id = x['values'][0]['id']


	'test : creating a symptom'
	x = test_post("/symptom",{'name': 'SYMPTOM TEST', 'description': 'Description is string'})
	symptom_id = x['values'][0]['id']


	'test : create a question'
	x = test_post("/question",{'name': 'QUESTION TEST', 'description': 'Description is string', 'dueanswer': '2020-01-01', 'metaanswer': '{ "my" : "meta" , "json" : "example" }'})
	question_id = x['values'][0]['id']

	'test : create a location'
	x = test_post("/location",{'latitude': '100', 'longitude': '100', 'name': 'braganca'})
	location_id = x['values'][0]['id']

	'test : disease has symptom'
	test_post(f"/has/{disease_id}/{symptom_id}",{"maxvalue":1,"minvalue":0.2})

	'test : disease require info'
	test_post(f"/require/{disease_id}/{question_id}",{"maxvalue":1,"minvalue":0.2})

	'test : symptom ask question'
	test_post(f"/ask/{symptom_id}/{question_id}",{})

	'test : person feel symptom'
	test_post(f"/feel/{person_id}/{symptom_id}",{"answer":0.5,"datetime":"2020-01-20"})

	'test : person info question'
	test_post(f"/info/{person_id}/{question_id}",{"answer":0.5,"datetime":"2020-01-20"})

	'test : person at location'
	test_post(f"/at/{person_id}/{location_id}",{"datetime":"2020-01-20"})

	'test : person answer question'
	test_post(f"/answer/{person_id}/{question_id}",{"answer":0.5,"datetime":"2020-01-20"})

	'test : next question'
	test_get(f"/get_next_question?person_id={person_id}")

	'test : rank'
	test_get(f"/rank_disease?person_id={person_id}")

	'test : rank location'
	test_get("/rank_simptom_by_location?datetime=2019-12-17&qtdays=100&radius=100&latitude=100&longitude=100")

	'test : person history'
	test_get(f"/history_symptons?person_id={person_id}")


def test_quiz():
	person_id = int(input("id_person:"))
	while(True):
		test_get(f"/rank_disease?person_id={person_id}")
		q = test_get(f"/get_next_question?person_id={person_id}")
		question_id = q['value'][0]['question_id']
		print("="*60)
		ans = float(input("ans:"))
		#print("="*60)
		test_post(f"/answer/{person_id}/{question_id}",{"answer":ans,"datetime":"2021-01-24"})
		print("="*60)
		


test_quiz()
#tests()



