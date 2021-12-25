import argparse
import json
from datetime import datetime as dt
from utils.api import get_schedule


def search_code(station):
	with open("only_spb_trains.json", "r") as f:
		stations = json.load(f)["stations"]
	for st in stations:
		if station in st["title"]:
			return st
	return None


def pretty_print(lines):
	max_length = max(len(x) for x in lines)

	print("┌" + "─" * max_length + "┐")
	i = 0
	for line in lines:
		print("│" + line + " "*(max_length - len(line)) + "│\n", end="")
		i += 1
		if len(lines) != 2 and i % 2 == 0 and i != len(lines):
			print("├" + "─" * max_length + "┤\n", end="")
	print("└" + "─" * max_length + "┘")


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Программа поиска расписания электричек по указанному маршруту.")
	parser.add_argument('-s', dest="start", help="Станция отправления", required=True, type=str)
	parser.add_argument('-t', dest="target", help="Станция прибытия", required=True, type=str)
	parser.add_argument('-d', default=dt.strftime(dt.now(), "%Y-%m-%d"),
						dest="date", help="Дата, для которой показывается расписание (в формате ГГГГ-ММ-ДД). По умолчанию - текущая дата",
						required=False,
						type=str)
	args = parser.parse_args()

	try:
		dt.strptime(args.date, "%Y-%m-%d")
		start = search_code(args.start)
		target = search_code(args.target)
		# print(start, target)
		if start and target:
			all_data, subs = get_schedule(start["yandex_code"], target["yandex_code"], args.date)
			if len(subs) != 0:
				# PRINTING DATA SECTION
				# print(subs)
				print(" Отправление: ", start['title'])
				print(" Прибытие:    ", target['title'])
				print(" Дата:        ", args.date)
				print(f" Ближайшая электричка:")
				ln1 = f" {start['title']} [{subs[0]['departure']}] - {target['title']} [{subs[0]['arrival']}] "
				ln2 = f" Поезд: {subs[0]['train']} {subs[0]['route']}, Стоимость: {subs[0]['price']} {subs[0]['currency']} "
				pretty_print([ln1, ln2])

				print(" Остальные электрички:")
				lines = []
				for s in range(1, len(subs)):
					lines.append(f" {start['title']} [{subs[s]['departure']}] - {target['title']} [{subs[s]['arrival']}] ")
					lines.append(f" Поезд: {subs[s]['train']} {subs[s]['route']}, Стоимость: {subs[s]['price']} {subs[s]['currency']} ")
				pretty_print(lines)
			else:
				pretty_print([" ОШИБКА: Для введенных станций не существует прямого пути без пересадок"])
		else:
			pretty_print([" ОШИБКА: Станции введены неверно"])
	except ValueError:
		pretty_print([" ОШИБКА: Неверный формат ввода даты"])