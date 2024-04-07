from abc import ABC, abstractmethod
from quiz.answer import Answer
import os


class Question(ABC):
	def __init__(self, text, answer_text, answers: list[Answer] | None = None):
		self.score = os.environ["SCORE_LOW"]
		self.text = text
		self.answer_text = answer_text
		self.answers = answers
		if answers is None:
			self.answers = []

	def ask(self) -> bool:
		user_input = input(self.text + ' ')

		try:
			is_right = user_input == self.answer_text
			hint = ''
			for ans in self.answers:
				is_right = ans.check(user_input)
				if is_right:
					self.score = ans.score
				hint = ans.get_hint(user_input)

			if is_right:
				print('A válasz helyes!')
			else:
				print(f'A válasz helytelen. A helyes válasz {self.answer_text} lett volna. {hint}')
			return is_right
		except AssertionError:
			return self.ask()

	def get_score(self):
		return self.score

	@abstractmethod
	def check_answer(self, user_input) -> (bool, str):
		pass


class NumberQuestion(Question):
	def check_answer(self, user_input) -> (bool, str):
		try:
			user_input = self.check_value(user_input)
			if user_input == self.answer_text:
				return True, ''
			else:
				return False, f'Eltérés: {user_input - self.answer_text:.3g}'
		except Exception as wtf:
			print(f'Hibás formátum.. A válaszod egész szám legyen! {wtf}')
			raise AssertionError

	@abstractmethod
	def check_value(self, user_input):
		pass
