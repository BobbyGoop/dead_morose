import requests
import json
import os


headers = {
	"Authorization": os.getenv('API_TOKEN')
}

params = {
	"lang": "ru",
	"format": "json"
}


def get_full_data():
	res = requests.get("https://api.rasp.yandex.net/v3.0/stations_list/", headers=headers)
	with open("../all_regions.json", "w") as f:
		json.dump(res.json(), f, indent=4,  ensure_ascii=False)
	print(res.status_code)


def extract_current_region():
	with open("../all_regions.json", "r") as f:
		spb = json.load(f)['countries'][29]['regions'][53]
	with open("../only_spb.json", "w") as f:
		json.dump(spb, f, indent=4, ensure_ascii=False)


def extract_stations():
	only_train = []
	with open("../only_spb.json", "r") as f:
		settlements = json.load(f)
		for s in settlements["settlements"]:
			for st in s ["stations"]:
				if st["transport_type"] in ["train", "suburban"]:
					only_train.append({
						"title": st["title"],
						"direction": st["direction"],
						"yandex_code": st["codes"]["yandex_code"],
						"transport_type": st["transport_type"]
					})

	with open("../only_spb_trains.json", "w") as f:
		json.dump({"stations" : only_train}, f, indent=4, ensure_ascii=False)


if __name__ == "__main__":
	get_full_data()
	extract_current_region()
	extract_stations()
	print("Extraction done.")