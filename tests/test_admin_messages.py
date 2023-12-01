import unittest
from unittest.mock import MagicMock
from src.bot import (
    handle_admin,
    handle_spam_text,
    AdminStates,
)

class TestAdminFunctions(unittest.TestCase):

    def setUp(self):
        self.bot = MagicMock()
        self.message = MagicMock()
        self.message.from_user.id = 123  # Замените на ваш реальный ADMIN_ID
        self.message.text = "Текст для рассылки"
        self.db = MagicMock()

    async def send_message_mock(self, user_id, text):
        pass

    async def test_handle_admin(self):
        # Подготовка теста
        self.message.from_user.id = 123
        with unittest.mock.patch('src.bot', self.bot):
            await handle_admin(self.message)
            self.bot.send_message.assert_called_once_with(
                self.message.from_user.id,
                "Напишите сообщение, которое будет разослано всем пользователям бота"
            )

    async def test_handle_spam_text(self):
        self.db.get_all_ids.return_value = [(1,), (2,), (3,)]
        with unittest.mock.patch('src.bot', self.bot), \
             unittest.mock.patch('src.db', self.db), \
             unittest.mock.patch('time.sleep', MagicMock()):
            await handle_spam_text(self.message, None)
            self.assertEqual(self.bot.send_message.call_count, 3)
            self.bot.send_message.assert_any_call(1, self.message.text)
            self.bot.send_message.assert_any_call(2, self.message.text)
            self.bot.send_message.assert_any_call(3, self.message.text)

if __name__ == '__main__':
    unittest.main()