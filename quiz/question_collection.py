from quiz.answer_collection import AnswerCollection
from quiz.question import Question, Hint
from quiz.answer import Answer, Tolerant
from quiz.tolerance import Tolerance, DecimalTolerance, PercentageTolerance, ConstTolerance
import quiz.question_types as qt


class QuestionCollection:
	def __init__(self, questions_data):
		self.questions = questions_data
		self.i = 0

	def __iter__(self):
		self.i = 0
		return self

	def __next__(self) -> Question:
		if self.i < len(self.questions):
			question_data = self.questions[self.i]
			self.i += 1

			question = self.create_question(question_data)

			if question != {}:
				return question
		else:
			raise StopIteration

		return question

	def create_question(self, question_data) -> Question:
		q = None
		if 'text' == question_data['type']:
			q = qt.RegexQuestion(question_data['text'], question_data['answer'], question_data['regex'])

		answers = self.create_answers(question_data)

		if 'number' == question_data['type']:
			q = qt.IntQuestion(question_data['text'], question_data['answer'], answers)
		if 'float' == question_data['type']:
			q = qt.FloatQuestion(question_data['text'], question_data['answer'], answers)
		if 'date' == question_data['type']:
			q = qt.DateQuestion(question_data['text'], question_data['answer'], answers)
		if 'date_strict' == question_data['type']:
			q = qt.DateQuestion(question_data['text'], question_data['answer'], answers)
		if 'bool' == question_data['type']:
			q = qt.BoolQuestion(question_data['text'], question_data['answer'], answers)

		# q = qt.FloatQuestion("asd", 6.7)

		if question_data.get('hint'):
			q.set_hint(Hint(question_data['hint']))

		return q

	def create_answers(self, question_data) -> AnswerCollection:
		answer_data = {}

		print(question_data)

		if question_data.get('tolerance'):
			tt = self.get_tolerance_type(question_data)
			answer_data. .(Tolerant(
				question_data['text'],
				question_data['answer'],
				self.create_tolerance(question_data, question_data, tt)
			))
			return answers

		if question_data.get('answers'):
			for answer_data in question_data['answers']:
				if answer_data is list:
					for ans in answer_data:
						answers.append(Answer(question_data['text'], ans))

				if answer_data is object:
					if answer_data.regex:
						answers.append(Answer(question_data['text'], answer_data['regex']))

					if answer_data.answer:
						tt = self.get_tolerance_type(answer_data)
						tolerance = self.create_tolerance(answer_data, question_data, tt)

						if tolerance is Tolerance:
							answers.append(Tolerant(
								question_data['text'],
								answer_data['answer'],
								tolerance
							))
		return AnswerCollection(answer_data)

	def create_tolerance(self, answer_data, question_data, tt):
		tolerance = None

		score = answer_data.get('score', 'low')

		if tt == 'decimal':
			tolerance = DecimalTolerance(question_data['text'], answer_data['tolerance']['decimal'], score)
		if tt == 'percent':
			tolerance = PercentageTolerance(question_data['text'], answer_data['tolerance']['percent'], score)
		if tt == 'const':
			tolerance = ConstTolerance(question_data['text'], answer_data['tolerance']['const'], score)
		return tolerance

	def get_tolerance_type(self, data):
		tt = ''
		if data.get('tolerance'):
			if data['tolerance'].get('const'):
				tt = 'const'
			if data['tolerance'].get('percent'):
				tt = 'percent'
			if data['tolerance'].get('decimal'):
				tt = 'decimal'
		return tt
