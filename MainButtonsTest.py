import unittest
from unittest.mock import Mock, patch

from bot import handle_main_buttons, go_back_to_mainmenu_keyboard, schedule_keyboard


class TestHandleMainButtons(unittest.TestCase):
    @patch('your_module.CokStates.waiting_for_fio.set')
    async def test_handle_main_buttons_cok(self, mock_set):
        message = Mock()
        message.text = "Написать письмо в ЦКО"
        message.from_user.id = 12345
        bot = Mock()
        await handle_main_buttons(message, bot)
        bot.send_message.assert_called_with(12345, "В этом разделе ты можешь написать письмо в Центр Качества Образования. \n\nДля обратной связи укажи свои данные.", reply_markup=go_back_to_mainmenu_keyboard)
        bot.send_message.assert_called_with(12345, "Введи своё ФИО:", reply_markup=go_back_to_mainmenu_keyboard)
        mock_set.assert_called()

    @patch('your_module.AskStates.waiting_for_question.set')
    async def test_handle_main_buttons_ask(self, mock_set):
        message = Mock()
        message.text = "Задать вопрос боту"
        message.from_user.id = 12345
        bot = Mock()
        await handle_main_buttons(message, bot)
        bot.send_message.assert_called_with(12345, "Введи свой вопрос:", reply_markup=go_back_to_mainmenu_keyboard)
        mock_set.assert_called()

    @patch('your_module.ScheduleStates.wait_for_week_or_day.set')
    async def test_handle_main_buttons_schedule(self, mock_set):
        message = Mock()
        message.text = "Получить расписание"
        message.from_user.id = 12345
        bot = Mock()
        await handle_main_buttons(message, bot)
        bot.send_message.assert_called_with(12345, text="Ты можешь получить расписание на сегодня или на неделю", reply_markup=schedule_keyboard)
        mock_set.assert_called()

if __name__ == '__main__':
    unittest.main()