from abc import ABC, abstractmethod
from quiz.answer import Answer
import os


class Hint:
	def __init__(self, text: str):
		self.text = text

	def get_hint(self, user_input: str) -> str:
		return f'Oké {user_input}, {self.text} lett volna'


class Question(ABC):
	def __init__(self, text: str, answer_text: str, answers: list[Answer] | None = None, hint: str | None = None):
		self.score = os.environ["SCORE_LOW"]
		self.text = text
		self.answer_text = answer_text
		self.answers = answers
		self.hint = None
		if hint:
			self.set_hint(Hint(hint))

	def ask(self) -> bool:
		user_input = input(self.text + ' ')

		try:
			is_right, hint = self.check_answer(user_input)

			if hint is not Hint and self.hint is Hint:
				hint = self.hint.get_hint(user_input)

			if is_right:
				print('A válasz helyes!')
				print(f'A válasz helytelen. A helyes válasz {self.answer_text} lett volna. {hint}')
			return is_right
		except AssertionError as er:
			print(f"{er}")
			return False

	def get_score(self):
		return self.score

	def set_hint(self, hint: Hint):
		self.hint = hint

	def check_answer(self, user_input: str) -> (bool, str | None):
		is_right = user_input == self.answer_text

		if is_right:
			return True, None

		hint = None
		for ans in self.answers:
			try:
				is_right = ans.check(user_input)
				if is_right:
					self.answer_text = ans.text
					self.score = ans.score

				if ans is Hint:
					hint = ans.get_hint(user_input)
			except ValueError:
				raise AssertionError

		return is_right, hint

	def get_answer_text(self) -> str:
		return self.answer_text

	def get_hint(self):
		return self.hint


class NumberQuestion(Question):
	@abstractmethod
	def check_value(self, user_input):
		pass
