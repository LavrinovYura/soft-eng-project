import unittest

from src.utils.similarity import Similarity


class TestSimilarityMethods(unittest.TestCase):

    def test_find_suitable_answer(self):
        # Проверка поиска подходящего ответа
        similarity = Similarity()
        test_question = "Какая формула Ньютона для гравитации?"
        expected_answer = "Такого вопроса нам еще не задавали. Тебе повезло, ты первый!"
        result = similarity.find_suitable_answer(test_question)
        self.assertEqual(result, expected_answer)

    def test_find_suitable_answer(self):
        # Проверка поиска подходящего ответа
        similarity = Similarity()
        test_question = "концерты"
        expected_answer = "https://whitehall.spbstu.ru/"
        result = similarity.find_suitable_answer(test_question)
        self.assertEqual(result, expected_answer)


if __name__ == '__main__':
    unittest.main()