import os
import smtplib
from email.mime.text import MIMEText

# Почта Mail.ru и пароль
mailru_user = "polynavibot@mail.ru"  # Замените на ваш адрес на Mail.ru
mailru_password = os.getenv('MAIL_PASSWORD')  # Установите переменную окружения MAILRU_PASSWORD

# Почта получателя
to = "pal4ik228@mail.ru"

def send_mail(question, mail, fio):
    msg = MIMEText(question + f"\n\nПожалуйста, пришлите ответ на почту: {mail}\n\n\nПисьмо сформировано при помощи " \
                         f"телеграм-бота для помощи студентам.")
    msg['Subject'] = "Вопрос в ЦКО от " + fio
    msg['From'] = mailru_user
    msg['To'] = to
    try:
        with smtplib.SMTP_SSL('smtp.mail.ru', 465) as server:
            server.login(mailru_user, os.getenv('GMAIL_PASSWORD'))
            server.send_message(msg)
        return "The message was sent!"
    except Exception as _ex:
        return f"{_ex}\n Something went wrong!"