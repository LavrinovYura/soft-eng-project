import unittest
from unittest.mock import Mock, patch
from python.bot import *

class TestBotHandlers(unittest.TestCase):

    @patch('python.dp')
    @patch('python.bot')
    async def test_handle_main_buttons(self, mock_bot, mock_dp):
        message_1 = Mock(text="Написать письмо в ЦКО")
        message_2 = Mock(text="Задать вопрос боту")
        message_3 = Mock(text="Получить расписание")
        messages = [message_1, message_2, message_3]

        # Testing "Написать письмо в ЦКО"
        await handle_main_buttons(messages[0])
        mock_bot.send_message.assert_called_with(
            message_1.from_user.id,
            "В этом разделе ты можешь написать письмо в Центр Качества Образования. \n\n"
            "Для обратной связи укажи свои данные.",
            reply_markup=mock_bot.types.ReplyKeyboardMarkup.return_value
        )
        mock_bot.send_message.reset_mock()

        # Testing "Задать вопрос боту"
        await handle_main_buttons(messages[1])
        mock_bot.send_message.assert_called_with(
            message_2.from_user.id,
            "Введи свой вопрос:",
            reply_markup=mock_bot.types.ReplyKeyboardMarkup.return_value
        )
        mock_bot.send_message.reset_mock()

        # Testing "Получить расписание"
        await handle_main_buttons(messages[2])
        mock_bot.send_message.assert_called_with(
            message_3.from_user.id,
            text="Ты можешь получить расписание на сегодня или на неделю",
            reply_markup=mock_bot.types.ReplyKeyboardMarkup.return_value
        )

    @patch('python.dp')
    @patch('python.bot')
    async def test_handle_schedule(self, mock_bot, mock_dp):
        mock_fsm_context = Mock()

        message_1 = Mock(text=go_back_text)
        message_2 = Mock(text="Получить расписание на сегодня")
        message_3 = Mock(text="Получить расписание на неделю")
        messages = [message_1, message_2, message_3]

        # Testing "go_back_text"
        await handle_schedule(messages[0], mock_fsm_context)
        mock_bot.send_message.assert_called_with(
            message_1.from_user.id,
            text=main_menu_text,
            reply_markup=mock_bot.types.ReplyKeyboardMarkup.return_value
        )
        mock_fsm_context.finish.assert_called_once()

        # Testing "Получить расписание на сегодня"
        await handle_schedule(messages[1], mock_fsm_context)
        mock_bot.send_message.assert_called_with(
            message_2.from_user.id,
            text=mock_bot.get_today_schedule.return_value,
            parse_mode='HTML',
            reply_markup=mock_bot.types.ReplyKeyboardMarkup.return_value
        )
        mock_fsm_context.finish.assert_called_once()

        # Testing "Получить расписание на неделю"
        await handle_schedule(messages[2], mock_fsm_context)
        mock_bot.send_message.assert_called_with(
            message_3.from_user.id,
            text=mock_bot.get_schedule.return_value,
            parse_mode='HTML',
            reply_markup=mock_bot.types.ReplyKeyboardMarkup.return_value
        )
        mock_fsm_context.finish.assert_called_once()

if __name__ == '__main__':
    unittest.main()