import requests

base = lambda x : f"http://127.0.0.1:5000/v1{x}"

def test_post(url,jsn):
	res = requests.post( base(url) , json = jsn)
	print(res.status_code,res.content)


test_post('/person/',{"name":"my first post"})
