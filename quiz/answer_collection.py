from quiz.answer import Answer, Tolerant
from quiz.tolerance import Tolerance


class AnswerCollection:
	def __init__(self, answer_data: list[dict | list[str] | object]):
		self.data = answer_data
		self.i = 0

	def __iter__(self):
		self.i = 0
		return self

	def __next__(self) -> Answer:
		if self.i < len(self.data):
			ans = self.data[self.i]

			if ans is list[str]:
				for text in ans:
					answer = Answer('', text)

			if ans is object:
				if ans.get('regex'):
					answer = Answer('', ans['regex'])

				if ans.get('answer'):
					tt = self.get_tolerance_type(answer_data)
					tolerance = self.create_tolerance(ans, question_data, tt)

					if tolerance is Tolerance:
						answer = Tolerant(
							question_data['text'],
							ans['answer'],
							tolerance
						)

			self.i += 1

			return answer

		else:
			raise StopIteration
