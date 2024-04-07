# pontrendszert kialakítani,
# a kérdéseket json fájlból olvassa be
# ABCD kérdéstípust berakni

import json
import os
from quiz.question_collection import QuestionCollection


def score(level: str) -> int:
	match level:
		case "low":
			return int(os.environ["SCORE_LOW"])
		case "default":
			return int(os.environ["SCORE_DEFAULT"])
		case "high":
			return int(os.environ["SCORE_HIGH"])
	return 0


'''
################### MAIN
'''

try:
	with open('questions.json', encoding='UTF-8') as questions_file:
		questions_json = json.load(questions_file)
except FileNotFoundError as FNFE:
	print(f'A {FNFE}fájl nem található')

player_name = 'asdasd'  ## input('Add meg a neved: ')
print(f'Szia {player_name}! Üdvözöllek a kvízjátékban! Sok sikert!')

no_q = 0
hits = 0
points = 0
results = []

for question in QuestionCollection(questions_json):
	no_q += 1
	if question.ask():
		hits += 1
		points += score(question.score())
		results.append(question.score())

print(f'\nJátékos neve: {player_name}')
print(f'A helyes válaszok száma {hits} / {no_q} ')
print(f'Pontszám: {points} / {no_q} pont.')
print(f'Eredmény: {100 * points / no_q:.3g} %')

with open('solution.json', 'a', encoding='UTF-8') as result_file:
	json.dump(results, result_file, indent=4)
	result_file.write(f'\nJátékos neve: {player_name}\n')
	result_file.write(f'A helyes válaszok száma {hits} / {no_q} \n')
	result_file.write(f'Pontszám: {points} / {no_q} pont.\n')
	result_file.write(f'Eredmény: {100 * points / no_q:.3g} %\n\n')
