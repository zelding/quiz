import datetime
import re
from quiz.question import Question, NumberQuestion


class RegexQuestion(Question):
	def __init__(self, text, answer_text, regex):
		super().__init__(text, answer_text)
		self.minta = regex

	def check_answer(self, user_input) -> (bool, str):
		try:
			return bool(re.search(self.minta, user_input)), ''
		except Exception as wtf:
			print(f'Hibás formátum! {wtf}')
			raise AssertionError


class IntQuestion(NumberQuestion):
	def check_value(self, user_input) -> int:
		try:
			return int(user_input)
		except Exception as ex:
			print('')
			raise ex


class FloatQuestion(NumberQuestion):
	def check_value(self, user_input: str) -> float:
		return float(user_input)

	def check_answer(self, user_input: str) -> (bool, str):
		try:
			user_input = self.check_value(user_input)
			if user_input == float(self.answer_text):
				return True, ''
			else:
				return False, f'{self.answer_text}'
		except Exception as wtf:
			print(f'Hibás formátum.. A válaszod egész szám legyen! {wtf}')
			raise AssertionError


class DateQuestion(Question):
	def check_answer(self, user_input) -> (bool, str):
		try:
			user_date = datetime.date.fromisoformat(user_input)
			answer = datetime.date.fromisoformat(self.answer_text)
			if user_date == answer:
				return True, ''
			else:
				return False, f'Eltérés: {(user_date - answer).days} nap'
		except Exception as wtf:
			print(f'Hibás formátum.. {wtf} A helyes formátum pl. (2024-04-04)')
			raise AssertionError


class BoolQuestion(NumberQuestion):
	def check_value(self, user_input) -> str:
		return str(user_input).lower()

	def check_answer(self, user_input) -> (bool, str):
		try:
			user_input = self.check_value(user_input)
			if user_input == self.answer_text:
				return True, ''
			else:
				return False, f'{self.answer_text}'
		except Exception as wtf:
			print(f'Hibás formátum.. A válaszod egész szám legyen! {wtf}')
			raise AssertionError