from abc import ABC, abstractmethod
import os

from quiz.tolerance import Tolerance


class Answer(ABC):
	@property
	def score(self) -> str:
		return self._score

	def __init__(self, text, answer):
		self.text = text
		self.answer = answer
		self._score = os.environ["SCORE_LOW"]

	def check(self, user_input) -> int:
		user_input = str.strip(user_input)
		user_input = self.convert_input(user_input)
		if user_input == self.answer:
			return True
		return False

	def __call__(self, *args, **kwargs):
		pass

	@abstractmethod
	def convert_input(self, user_input):
		pass

	@score.setter
	def score(self, value: str):
		self._score = value


class Tolerant(Answer, ABC):
	def __init__(self, text, answer, tolerance: Tolerance | None):
		super().__init__(text, answer)
		self.tolerance = tolerance

	def check(self, user_input) -> bool:
		if super().check(user_input):
			return True

		if self.tolerance is Tolerance:
			return self.tolerance(user_input)

		return False
