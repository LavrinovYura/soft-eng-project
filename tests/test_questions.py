import unittest
from unittest.mock import Mock, patch
from python.bot import (
    handle_question,
    handle_yes_no,
    handle_yes_no_two,
    main_keyboard, sm
)

class TestAskHandlers(unittest.TestCase):

    @patch("src.bot.send_message")
    async def test_handle_question_go_back(self, mock_send_message):
        message = Mock()
        state = Mock()
        message.text = "Назад"
        await handle_question(message, state)
        state.finish.assert_called_once()
        mock_send_message.assert_called_with(
            message.from_user.id,
            text="Главное меню",
            reply_markup=main_keyboard
        )

    @patch("src.bot.send_message")
    async def test_handle_yes_no_go_back(self, mock_send_message):
        message = Mock()
        state = Mock()
        message.text = "Назад"
        await handle_yes_no(message, state)
        state.finish.assert_called_once()
        mock_send_message.assert_called_with(
            message.from_user.id,
            text="Главное меню",
            reply_markup=main_keyboard
        )

    @patch("src.bot.send_message")
    async def test_handle_yes_no_two_go_back(self, mock_send_message):
        message = Mock()
        state = Mock()
        message.text = "Назад"
        await handle_yes_no_two(message, state)
        mock_send_message.assert_called_with(
            message.from_user.id,
            text="Главное меню",
            reply_markup=main_keyboard
        )
        state.finish.assert_called_once()

    @patch("your_module.bot.send_message")
    async def test_handle_yes_no_get_answer(self, mock_send_message):
        message = Mock()
        state = Mock()
        message.text = "Да"
        await handle_yes_no(message, state)
        mock_send_message.assert_called_with(
            message.from_user.id,
            text="Отлично!\nГлавное меню",
            reply_markup=main_keyboard
        )
        state.finish.assert_called_once()

    @patch("your_module.bot.send_message")
    async def test_handle_yes_no_two_search_similar(self, mock_send_message):
        message = Mock()
        state = Mock()
        message.text = "Нет"
        user_data = {'question': 'Sample question'}
        state.get_data.return_value = user_data
        sm.get_top_questions.return_value = (['Q1', 'Q2', 'Q3'], ['A1', 'Null', 'A3'])

        await handle_yes_no_two(message, state)

        mock_send_message.assert_called_with(
            message.from_user.id,
            text="Возможно, ты искал:\n\nQ1\nA1\n\nQ3\nA3",
        )
        state.finish.assert_not_called()

if __name__ == "__main__":
    unittest.main()