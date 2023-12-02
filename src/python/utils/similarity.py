import os
from db.database import Database
from difflib import SequenceMatcher
from dotenv import load_dotenv
load_dotenv()
class Similarity:
    # Поиск подходящего ответа
    def find_suitable_answer(self, question):
        db_file = os.getenv('PATH_DB')
        db = Database(db_file)
        max_ratio = 0
        answer = "Такого вопроса нам еще не задавали. Тебе повезло, ты первый!"
        for db_question in db.get_all_questions():
            ratio = SequenceMatcher(None, question, str(db_question[0]).lower()).ratio()
            if ratio > max_ratio and ratio > 0.6:
                answer = db.get_answer(db_question[0])
                max_ratio = ratio
        db.close()
        return answer

    # Получение топа вопросов по похожести
    def get_top_questions(self, question):
        db_file = "resources/dataBaseStudents.db"
        db = Database(db_file)
        max_ratios = [0] * 3
        answers = ['Null'] * 3
        questions = [''] * 3
        for db_question in db.get_all_questions():
            ratio = SequenceMatcher(None, question, str(db_question[0]).lower()).ratio()
            if ratio > min(max_ratios):
                index = max_ratios.index(min(max_ratios))
                max_ratios[index] = ratio
                answers[index] = db.get_answer(db_question[0])
                questions[index] = db_question[0]
        db.close()
        return questions, answers
