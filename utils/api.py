import requests
from datetime import datetime as dt
import os


def get_schedule(code_start, code_target, date):
	headers = {
		"Authorization": os.getenv('API_TOKEN')
	}

	params = {
		"from": code_start,
		"to": code_target,
		"limit": 50,
		"date": date,
		"transfers": False
	}

	res = requests.get("https://api.rasp.yandex.net/v3.0/search/", headers=headers, params=params)
	data = res.json()

	# print(json.dumps(res.json(), indent=4, ensure_ascii=False))
	# print(res.status_code)

	subs = []
	for travel in data["segments"]:
		dep_time = dt.strptime(travel["departure"][0:19], "%Y-%m-%dT%H:%M:%S")
		arr_time = dt.strptime(travel["arrival"][0:19], "%Y-%m-%dT%H:%M:%S")
		if dep_time > dt.now():
			subs.append({
				"from": {
					"title": travel["from"]["title"],
					"code" : travel["from"]["code"]
				},
				"to": {
					"title": travel["to"]["title"],
					"code": travel["to"]["code"]
				},
				"departure": str(dep_time),
				"arrival": str(arr_time),
				"route": travel["thread"]["title"],
				"train": travel["thread"]["number"],
				"currency": f' {travel["tickets_info"]["places"][0]["currency"]}',
				"price": f'{travel["tickets_info"]["places"][0]["price"]["whole"]}'

			})

	# print(json.dumps(subs, indent=4, ensure_ascii=False))
	return data, subs
