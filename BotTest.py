import asyncio
import unittest
from bot import dp, db, handle_start, handle_schedule, help_text, handle_messages, message_is_group
from aiogram import types

class TestBotFunctionality(unittest.TestCase):

    def setUp(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def tearDown(self):
        self.loop.close()

    def test_handle_start_new_user(self):
        async def test():
            # Создаем объект сообщения с использованием aiogram
            message = types.Message()
            message.text = '/start'
            message.from_user = types.User(id=123)

            # Вызываем функцию обработки старта
            await handle_start(message)

            # Проверяем, что бот отправил правильные сообщения
            expected_messages = [
                types.Message(
                    text="Привет! Я твой персональный помощник, способный ответить на твой вопрос об обучении в Политехе!",
                    chat=message.from_user.id),
                types.Message(text="Чтобы начать работу, отправь мне свой номер группы:", chat=message.from_user.id)
            ]

            self.assertEqual(dp.sent_messages, expected_messages)

            # Проверяем, что новый пользователь добавлен в БД
            self.assertTrue(db.user_exists(123))

    def test_handle_start_existing_user(self):
        async def test():
            # Создаем объект сообщения с использованием aiogram
            message = types.Message()
            message.text = '/start'
            message.from_user = types.User(id=123)

            # Добавляем существующего пользователя в БД
            db.add_user(123)

            # Очищаем список отправленных сообщений перед тестом
            dp.sent_messages = []

            # Вызываем функцию обработки старта
            await handle_start(message)

            # Проверяем, что бот отправил правильные сообщения
            assert dp.sent_messages == [
                types.Message(
                    text="Привет! Я твой персональный помощник, способный ответить на твой вопрос об обучении в Политехе!",
                    chat=message.from_user.id),
                types.Message(text="Чтобы начать работу, отправь мне свой номер группы:", chat=message.from_user.id)
            ]

            # Проверяем, что существующий пользователь не добавлен в БД второй раз
            self.assertEqual(db.get_user_count(), 1)

    def test_handle_schedule(self):
        async def test():
            # Создаем объект сообщения с использованием aiogram
            message = types.Message()
            message.text = '/help'
            message.from_user = types.User(id=123)

            # Очищаем список отправленных сообщений перед тестом
            dp.sent_messages = []

            # Вызываем функцию handle_schedule
            await handle_schedule(message)

            # Проверяем, что бот отправил правильное сообщение
            assert dp.sent_messages == [
                types.Message(text=help_text, chat=message.from_user.id, parse_mode='HTML')
            ]

    def test_handle_messages(self):
        async def test():
            # Создаем объект сообщения с использованием aiogram
            message = types.Message()
            message.text = 'Test message'
            message.from_user = types.User(id=123)

            # Очищаем список отправленных сообщений перед тестом
            dp.sent_messages = []

            # Вызываем функцию handle_messages
            await handle_messages(message)

            # Проверяем, что бот отправил правильное сообщение с текстом, идентичным входному сообщению
            assert dp.sent_messages == [
                types.Message(text=message.text, chat=message.from_user.id)
            ]

class TestMessageIsGroup(unittest.TestCase):

    def test_message_is_group_valid(self):
        # Проверяем, что корректное сообщение группы возвращает True
        text = "1234567/12345"
        result = message_is_group(text)
        self.assertTrue(result)

    def test_message_is_group_invalid(self):
        # Проверяем, что некорректное сообщение группы возвращает False
        invalid_text = "1234/12345"  # Неправильная длина первой части
        result = message_is_group(invalid_text)
        self.assertFalse(result)

        invalid_text = "1234567/1234"  # Неправильная длина второй части
        result = message_is_group(invalid_text)
        self.assertFalse(result)

        invalid_text = "abc/def"  # Не числовые значения
        result = message_is_group(invalid_text)
        self.assertFalse(result)

        invalid_text = "1234567/12345/extra"  # Лишняя часть
        result = message_is_group(invalid_text)
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()