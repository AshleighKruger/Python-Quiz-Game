from typing import List, Dict
from Data import questions


def get_questions(difficulty: str) -> List[Dict]:
	"""Return list of questions matching a difficulty."""
	return [q for q in questions if q.get("difficulty") == difficulty]


def check_answer(question: Dict, choice: int) -> bool:
	"""Return True when the provided choice index matches the question's correct_index."""
	return choice == question.get("correct_index")


def calculate_score(score: int, total: int) -> float:
	"""Return percentage score (0-100)."""
	if total <= 0:
		return 0.0
	return (score / total) * 100.0


def quiz_finished(current_question: int, total_questions: int) -> bool:
	"""Return True when the quiz is finished."""
	return current_question >= total_questions