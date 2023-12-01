import unittest
from unittest.mock import Mock, patch
from aiogram import types
from aiogram.dispatcher import FSMContext
from src.bot import handle_schedule, go_back_text

class TestHandleSchedule(unittest.TestCase):
    def setUp(self):
        self.bot = Mock()
        self.message = Mock(spec=types.Message)
        self.state = Mock(spec=FSMContext)

    def test_handle_schedule_go_back(self):
        self.message.text = go_back_text
        handle_schedule(self.message, self.state)

    def test_handle_schedule_get_today_schedule_success(self):
        self.message.text = "Получить расписание на сегодня"
        self.message.from_user.id = 123
        db = Mock()
        db.get_group_id.return_value = ["group1"]
        get_today_schedule = Mock(return_value="Today's schedule")
        with patch('src.bot.get_today_schedule', get_today_schedule), patch('src.bot.db', db):
            handle_schedule(self.message, self.state)

    def test_handle_schedule_get_today_schedule_exception(self):
        self.message.text = "Получить расписание на сегодня"
        self.message.from_user.id = 123
        db = Mock()
        db.get_group_id.return_value = ["group1"]
        get_today_schedule = Mock(side_effect=Exception("Invalid group"))
        with patch('src.bot.get_today_schedule', get_today_schedule), patch('src.bot.db', db):
            handle_schedule(self.message, self.state)

    def test_handle_schedule_get_schedule_success(self):
        self.message.text = "Получить расписание на неделю"
        self.message.from_user.id = 123
        db = Mock()
        db.get_group_id.return_value = ["group1"]
        get_schedule = Mock(return_value="Weekly schedule")
        with patch('src.bot.get_schedule', get_schedule), patch('src.bot.db', db):
            handle_schedule(self.message, self.state)

    def test_handle_schedule_get_schedule_exception(self):
        self.message.text = "Получить расписание на неделю"
        self.message.from_user.id = 123
        db = Mock()
        db.get_group_id.return_value = ["group1"]
        get_schedule = Mock(side_effect=Exception("Invalid group"))
        with patch('src.bot.get_schedule', get_schedule), patch('src.bot.db', db):
            handle_schedule(self.message, self.state)

    def test_handle_schedule_other_message(self):
        self.message.text = "Some other message"
        handle_schedule(self.message, self.state)

if __name__ == '__main__':
    unittest.main()