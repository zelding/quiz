from abc import ABC, abstractmethod


class Tolerance(ABC):
	def __init__(self, answer, threshold: int):
		self.answer = answer
		self.threshold = threshold

	def __call__(self, user_input):
		return self.check(user_input)

	@abstractmethod
	def check(self, user_input) -> bool:
		pass


class DecimalTolerance(Tolerance):
	def check(self, user_input) -> bool:
		abs_tolerance = min(abs(self.threshold), 1)

		if self.threshold > 0:
			return round(self.answer / user_input, self.threshold) == 1

		str_tolerance = self.threshold.__str__()
		str_answer = self.answer.__str__()

		ln_answer = len(str_answer)
		ln_tolerance = len(str_tolerance)
		abs_tolerance = max(abs_tolerance, min(ln_answer, ln_tolerance))
		abs_tolerance = min(abs_tolerance, max(ln_answer, ln_tolerance))
		return str_answer[:abs_tolerance] == str_tolerance[:abs_tolerance]


class PercentageTolerance(Tolerance):
	def check(self, user_input) -> bool:
		user_input = float(user_input)
		fl_answer = float(self.answer)
		fl_tolerance = self.threshold / 100.0
		return fl_answer * (1.0 + fl_tolerance) > user_input > fl_answer * fl_tolerance


class ConstTolerance(Tolerance):
	def check(self, user_input) -> bool:
		user_input = float(user_input)
		fl_answer = float(self.answer)
		fl_tolerance = self.threshold / 100.0
		return fl_answer + fl_tolerance > user_input > fl_answer - fl_tolerance
