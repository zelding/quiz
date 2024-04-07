# pontrendszert kialakítani,
# a kérdéseket json fájlból olvassa be
# ABCD kérdéstípust berakni

import json
import os
from quiz.question_collection import QuestionCollection

solution_file_name = os.environ['HISTORY_FILE'] or exit(-1)
question_file_name = os.environ['QUESTION_FILE'] or exit(-2)


def score(level: str) -> int:
	match level:
		case "low":
			return int(os.environ["SCORE_LOW"]) or exit(-3)
		case "default":
			return int(os.environ["SCORE_DEFAULT"]) or exit(-4)
		case "high":
			return int(os.environ["SCORE_HIGH"]) or exit(-5)
	return 0


if __name__ == '__main__':
	try:
		with open(question_file_name, encoding='UTF-8') as questions_file:
			questions_json = json.load(questions_file)
	except FileNotFoundError as err:
		print(f'A {err} fájl nem található')

	player_name = 'asdasd'  ## input('Add meg a neved: ')
	print(f'Szia {player_name}! Üdvözöllek a kvízjátékban! Sok sikert!')

	no_q = 0
	hits = 0
	points = 0
	results = []

	for question in QuestionCollection(questions_json):
		r = question.ask()
		if r:
			hits += 1
			points += score(question.score)
			results.append(question.score)

		no_q += 1
		if not r:
			results.append(0)

	no_q *= score("default")

	print(f'\nJátékos neve: {player_name}')
	print(f'A helyes válaszok száma {hits} / {no_q} ')
	print(f'Pontszám: {points} / {no_q} pont.')
	print(f'Eredmény: {100 * points / no_q:.3g} %')

	with open(solution_file_name, 'a', encoding='UTF-8') as result_file:
		json.dump(results, result_file, indent=4)
		result_file.write(f'\nJátékos neve: {player_name}\n')
		result_file.write(f'A helyes válaszok száma {hits} / {no_q} \n')
		result_file.write(f'Pontszám: {points} / {no_q} pont.\n')
		result_file.write(f'Eredmény: {100 * points / no_q:.3g} %\n\n')
