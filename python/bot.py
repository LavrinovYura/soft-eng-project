import logging
import os
import re
import time

from aiogram.utils.exceptions import ChatNotFound, BotBlocked
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from python.db.database import Database
from python.states.admin_states import *
from python.states.ask_states import *
from python.states.cok_states import *
from python.states.schedule_states import *
from python.states.start_state import *
from python.utils import mail_sender
from python.utils.ruz_parser import get_schedule, get_today_schedule
from python.utils.similarity import Similarity
from python.utils.groups_parser import is_group_in_list


# Инициализация логов
logging.basicConfig(level=logging.DEBUG)
load_dotenv()

# Инициализация бота
bot = Bot(token=os.getenv('TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

# # Инициализация БД
db = Database(os.getenv('PATH_DB'))

# Клавиатуры
help_button = types.KeyboardButton("Написать письмо в ЦКО")
question_button = types.KeyboardButton("Задать вопрос боту")
schedule_button = types.KeyboardButton("Получить расписание")
main_keyboard = types.ReplyKeyboardMarkup().add(help_button).add(question_button).add(schedule_button)

go_back_text = "Вернуться в главное меню"
go_back_button = types.KeyboardButton(go_back_text)
go_back_to_mainmenu_keyboard = types.ReplyKeyboardMarkup().add(go_back_button)

yes_button = types.KeyboardButton("Да")
no_button = types.KeyboardButton("Нет")
go_back_and_yes_no_keyboard = types.ReplyKeyboardMarkup().add(yes_button).add(no_button).add(go_back_button)

yes_go_search = "Да, искать похожие вопросы"
no_go_search = "Нет, вернуться в главное меню"
yes_search_button = types.KeyboardButton(yes_go_search)
no_go_back_button = types.KeyboardButton(no_go_search)
go_back_and_yes_search_keyboard = types.ReplyKeyboardMarkup().add(yes_search_button).add(no_go_back_button)

today_schedule_button = types.KeyboardButton("Получить расписание на сегодня")
week_schedule_button = types.KeyboardButton("Получить расписание на неделю")
schedule_keyboard = types.ReplyKeyboardMarkup().add(today_schedule_button).add(week_schedule_button).add(go_back_button)

# Текстики
main_menu_text = "С помощью кнопок ниже выбери, что хочешь сделать"
sorry_no_understand_text = "Не понял, выбери один из вариантов внизу"
help_text = "<b>PolyNaviBot</b> - это <u>уникальный бот</u>, способный помочь связаться с ЦКО или ответить на " \
            "волнующие вопросы\nЕсли мы мы не смогли найти ответ на вопрос, не переживай! Мы собираем все " \
            "интригующие аудиторию вопросы и на наиболее частые <b>даем ответ</b>!"

# Класс совпадений
sm = Similarity()




# Обработка старт
@dp.message_handler(commands=['start'])
async def handle_start(message: types.Message):
    if message.text == '/start':
        if db.user_exists(message.from_user.id):
            pass
        else:
            db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, text="Привет! Я твой персональный помощник, способный ответить "
                                                          "на твой вопрос об обучении в Политехе!")
        await bot.send_message(message.from_user.id, text="Чтобы начать работу, отправь мне свой номер группы:")
        await StartState.waiting_for_group_id.set()


# Продолжение после старт
@dp.message_handler(state=StartState.waiting_for_group_id)
async def handle_waiting_group(message: types.Message, state: FSMContext):
    if is_group_in_list(message.text):
        db.set_group_id(message.from_user.id, message.text.replace("/", "."))
        await bot.send_message(message.from_user.id, "Номер группы установлен.\n\n" + main_menu_text,
                               reply_markup=main_keyboard)
        await state.finish()
        return
    else:
        await bot.send_message(message.from_user.id, "Введи корректно номер группы в формате <b>XXXXXXX/XXXXX</b>",
                               parse_mode="HTML")
        return

# admin - рассылка всем
@dp.message_handler(commands=['admin'])
async def handle_admin(message: types.Message):
    if message.from_user.id in os.getenv('ADMIN_ID'):
        await bot.send_message(message.from_user.id,
                               "Напишите сообщение, которое будет разослано всем пользователям бота")
        await AdminStates.waiting_for_text.set()


# admin - получение текста для рассылки и отправка текста всем пользователям
@dp.message_handler(state=AdminStates.waiting_for_text)
async def handle_spam_text(message: types.Message, state: FSMContext):
    for user_id in db.get_all_ids():
        try:
            await bot.send_message(user_id[0], message.text)
            time.sleep(1)
        except (ChatNotFound, BotBlocked):
            continue
    await state.finish()

# Получение помощи
@dp.message_handler(commands=['help'])
async def handle_schedule(message: types.Message):
    await bot.send_message(message.from_user.id, text=help_text, parse_mode='HTML')


# Обработка main кнопок
@dp.message_handler()
async def handle_main_buttons(message: types.Message):
    if message.text == "Написать письмо в ЦКО":
        await bot.send_message(message.from_user.id,
                               "В этом разделе ты можешь написать письмо в Центр Качества Образования. \n\n"
                               "Для обратной связи укажи свои данные.",
                               reply_markup=go_back_to_mainmenu_keyboard)
        await bot.send_message(message.from_user.id, "Введи своё ФИО:", reply_markup=go_back_to_mainmenu_keyboard)
        await CokStates.waiting_for_fio.set()
    elif message.text == "Задать вопрос боту":
        await bot.send_message(message.from_user.id, "Введи свой вопрос:", reply_markup=go_back_to_mainmenu_keyboard)
        await AskStates.waiting_for_question.set()
    elif message.text == "Получить расписание":
        await bot.send_message(message.from_user.id, text="Ты можешь получить расписание на сегодня или на неделю", reply_markup=schedule_keyboard)
        await ScheduleStates.wait_for_week_or_day.set()


# Получение расписания на неделю или день
@dp.message_handler(state=ScheduleStates.wait_for_week_or_day)
async def handle_schedule(message: types.Message, state: FSMContext):
    if message.text == go_back_text:
        await state.finish()
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
    elif message.text == "Получить расписание на сегодня":
        try:
            schedule = get_today_schedule(db.get_group_id(message.from_user.id)[0].replace(".", "/"))
            await bot.send_message(message.from_user.id, text=schedule, parse_mode='HTML', reply_markup=main_keyboard)
        except Exception:
            await bot.send_message(message.from_user.id, text="Введен номер несуществующей группы. Чтобы изменить "
                                                              "номер группы, напиши /start", parse_mode='HTML',
                                   reply_markup=main_keyboard)
        await state.finish()
    elif message.text == "Получить расписание на неделю":
        try:
            schedule = get_schedule(db.get_group_id(message.from_user.id)[0].replace(".", "/"))
            await bot.send_message(message.from_user.id, text=schedule, parse_mode='HTML', reply_markup=main_keyboard)
        except Exception:
            await bot.send_message(message.from_user.id, text="Введен номер несуществующей группы. Чтобы изменить "
                                                              "номер группы, напиши /start", parse_mode='HTML',
                                   reply_markup=main_keyboard)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, text=sorry_no_understand_text)

# Обработка ФИО
@dp.message_handler(state=CokStates.waiting_for_fio)
async def handle_fio(message: types.Message, state: FSMContext):
    if message.text == go_back_text:
        await state.finish()
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
    else:
        if text_is_fio(message.text):
            await state.update_data(fio=message.text)
            await bot.send_message(message.from_user.id, text="Введи свой вопрос:")
            await CokStates.waiting_for_question.set()
        else:
            await bot.send_message(message.from_user.id,
                                   text="Введи корректно своё ФИО в формате <b>Иванов Иван Иванович</b>:",
                                   parse_mode='HTML')


# Обработка полученного вопроса
@dp.message_handler(state=CokStates.waiting_for_question)
async def handle_question_to_send(message: types.Message, state: FSMContext):
    if message.text == go_back_text:
        await state.finish()
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
    else:
        await state.update_data(question=message.text)
        await bot.send_message(message.from_user.id, text="Введи свою почту, чтобы получить на нее ответ:")
        await CokStates.waiting_for_mail.set()


# Обработка полученного mail'a
@dp.message_handler(state=CokStates.waiting_for_mail)
async def handle_mail(message: types.Message, state: FSMContext):
    if message.text == go_back_text:
        await state.finish()
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
    else:
        if message_is_mail(message.text):
            await state.update_data(mail=message.text)
            user_data = await state.get_data()
            question = user_data['question']
            await bot.send_message(message.from_user.id,
                                   text=f'Ты хочешь отправить письмо в ЦКО с вопросом:\n\n<b>{question}</b>\n\n'
                                        f'И получить ответ на почту: <b>{message.text}</b>\n\n'
                                        f'Все верно?', parse_mode='HTML', reply_markup=go_back_and_yes_no_keyboard)
            await CokStates.confirm_sending.set()
        else:
            await bot.send_message(message.from_user.id, text="Введи свою почту в верном формате!")


# Подтверждение отправления письма
@dp.message_handler(state=CokStates.confirm_sending)
async def handle_confirmation(message: types.Message, state: FSMContext):
    if message.text == go_back_text:
        await state.finish()
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
    elif message.text == 'Нет':
        await state.finish()
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
    elif message.text == 'Да':
        user_data = await state.get_data()
        mail = user_data['mail']
        question = user_data['question']
        fio = user_data['fio']
        mail_sender.send_mail(question, mail, fio)
        await bot.send_message(message.from_user.id, text="Письмо отправлено!")
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, text=sorry_no_understand_text)


# Обработка полученного вопроса
@dp.message_handler(state=AskStates.waiting_for_question)
async def handle_question(message: types.Message, state: FSMContext):
    if message.text == go_back_text:
        await state.finish()
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
    else:
        answer = sm.find_suitable_answer(message.text.lower())
        await bot.send_message(message.from_user.id, answer)
        if answer == "Такого вопроса нам еще не задавали. Тебе повезло, ты первый!":
            await bot.send_message(message.from_user.id, "Хочешь увидеть похожие вопросы??",
                                   reply_markup=go_back_and_yes_search_keyboard)
        else:
            await bot.send_message(message.from_user.id, "Ты получил ответ на свой вопрос?",
                                   reply_markup=go_back_and_yes_no_keyboard)
        await state.update_data(question=message.text)
        await AskStates.did_you_get_the_right_answer.set()


# Обработка "вы получили ответ на свой вопрос?" вывод топ 3 вопросов
@dp.message_handler(state=AskStates.did_you_get_the_right_answer)
async def handle_yes_no(message: types.Message, state: FSMContext):
    if message.text == go_back_text:
        await state.finish()
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
    elif message.text == "Да" or message.text == no_go_search:
        await bot.send_message(message.from_user.id, text="Отлично!\n" + main_menu_text, reply_markup=main_keyboard)
        await state.finish()
    elif message.text == "Нет" or message.text == yes_go_search:
        user_data = await state.get_data()
        await bot.send_message(message.from_user.id, text="Попробуем найти похожие вопросы из нашей базы...")
        questions, answers = sm.get_top_questions(user_data['question'])
        if answers[0] == "Null":
            result = 'Похожих вопросов не найдено :('
        else:
            result = "Возможно, ты искал:"
            for i in range(3):
                if answers[i] != "Null":
                    result = result + f"\n\n{questions[i]}\n{answers[i]}"
        await bot.send_message(message.from_user.id, text=result)
        await bot.send_message(message.from_user.id, text="Ты получил ответ на свой вопрос?",
                               reply_markup=go_back_and_yes_no_keyboard)
        await AskStates.did_you_get_the_right_answer_after_top.set()
    else:
        await bot.send_message(message.from_user.id, text=sorry_no_understand_text,
                               reply_markup=go_back_and_yes_no_keyboard)


# Обработка "Вы получили ответ на свой вопрос №2" добавление вопроса в бд
@dp.message_handler(state=AskStates.did_you_get_the_right_answer_after_top)
async def handle_yes_no_two(message: types.Message, state: FSMContext):
    if message.text == go_back_text:
        await bot.send_message(message.from_user.id, text=main_menu_text, reply_markup=main_keyboard)
        await state.finish()
    elif message.text == "Да":
        await bot.send_message(message.from_user.id, text="Отлично!\n" + main_menu_text, reply_markup=main_keyboard)
        await state.finish()
    elif message.text == "Нет":
        await bot.send_message(message.from_user.id, text="Нам жаль, мы добавим ваш вопрос на рассмотрение. "
                                                          "Чтобы получить ответ на данный вопрос быстрее, "
                                                          "воспользуйся функцией отправки письма в ЦКО в главном меню",
                               reply_markup=main_keyboard)
        user_data = await state.get_data()
        db.add_question_to_consider(user_data['question'])
        await state.finish()
    else:
        await bot.send_message(message.from_user.id, text=sorry_no_understand_text,
                               reply_markup=go_back_and_yes_no_keyboard)


# Обработка всех сообщений
@dp.message_handler()
async def handle_messages(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


# Проверка является ли текст-мейлом
def message_is_mail(message):
    if re.fullmatch(
            r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])",
            message):
        return True
    else:
        return False


# Проверка является ли текст фио
def text_is_fio(text):
    if len(text.split(" ")) == 3:
        return True
    else:
        return False


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
