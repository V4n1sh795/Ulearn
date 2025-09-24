import requests as rq
URL_GET = "http://127.0.0.1:8000/vacancies/1"
resp = rq.get(URL_GET)
inp = input()
if resp['area_name'] == inp:
    print(resp.json)