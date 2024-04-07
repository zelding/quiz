from abc import ABC, abstractmethod
import os

from quiz.tolerance import Tolerance


class Answer(ABC):
	@property
	def score(self) -> str:
		return self._score

	def __init__(self, text: str, answer: str):
		self.text = text
		self.answer = answer
		self._score = os.environ["SCORE_LOW"]

	@abstractmethod
	def check(self, user_input: str) -> int:
		user_input = self.convert_input(user_input)
		if user_input == self.answer:
			return True
		return False

	def __call__(self, *args, **kwargs):
		return self.check(*args)

	@abstractmethod
	def convert_input(self, user_input: str) -> str:
		return str.strip(user_input)

	@score.setter
	def score(self, value: str):
		self._score = value

	def get_answer(self) -> str:
		return self.answer


class Tolerant(Answer):
	def __init__(self, text: str, answer: str, tolerance: Tolerance):
		super().__init__(text, answer)
		self.tolerance = tolerance

	def check(self, user_input: str) -> bool:
		if super().check(user_input):
			return True

		is_ok = self.tolerance.check(user_input)

		if is_ok:
			self.score = self.tolerance.score

		return is_ok

	def convert_input(self, user_input: str) -> int:
		user_input = super().convert_input(user_input)
		return int(user_input)
