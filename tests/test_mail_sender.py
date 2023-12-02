import unittest
from unittest.mock import patch
from python.utils.mail_sender import send_mail

class TestMailSender(unittest.TestCase):
    @patch('smtplib.SMTP')
    def test_send_mail_successful(self, mock_smtp):
        # Успешная отправка письма
        result = send_mail("Проверочка!!!", "test@example.com", "Карасий Карпов Окуневич")

        self.assertEqual(result, "The message was sent!")

    @patch('smtplib.SMTP')
    def test_send_mail_failure(self, mock_smtp):
        # Перехват ошибки при отправке письма
        mock_smtp.return_value.login.side_effect = Exception("Mocked error")
        result = send_mail("Проверочка!!!", "test@example.com", "Карасий Карпов Окуневич")

        self.assertIn("Mocked error", result)
        self.assertIn("Something went wrong!", result)

if __name__ == '__main__':
    unittest.main()