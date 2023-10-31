import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext

from DataBase import DataBase
from StatesDir.StartState import *
from config import *

# Инициализация логов
logging.basicConfig(level=logging.DEBUG)

# Инициализация бота
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# # Инициализация БД
db_file = "dataBaseStudents.db"
db = DataBase(db_file)

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

# Текстики
main_menu_text = "С помощью кнопок ниже выбери, что хочешь сделать"
sorry_no_understand_text = "Не понял, выбери один из вариантов внизу"
help_text = "<b>PolyNaviBot</b> - это <u>уникальный бот</u>, способный помочь связаться с ЦКО или ответить на " \
            "волнующие вопросы\nЕсли мы мы не смогли найти ответ на вопрос, не переживай! Мы собираем все " \
            "интригующие аудиторию вопросы и на наиболее частые <b>даем ответ</b>!"

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
    if message_is_group(message.text):
        db.set_group_id(message.from_user.id, message.text.replace("/", "."))
        await bot.send_message(message.from_user.id, "Номер группы установлен.\n\n" + main_menu_text,
                               reply_markup=main_keyboard)
        await state.finish()
        return
    else:
        await bot.send_message(message.from_user.id, "Введи корректно номер группы в формате <b>XXXXXXX/XXXXX</b>",
                               parse_mode="HTML")
        return

# Получение помощи
@dp.message_handler(commands=['help'])
async def handle_schedule(message: types.Message):
    await bot.send_message(message.from_user.id, text=help_text, parse_mode='HTML')

# Обработка всех сообщений
@dp.message_handler()
async def handle_messages(message: types.Message):
    await bot.send_message(message.from_user.id, message.text)


# Проверка является ли текст - группой
def message_is_group(text):
    splitted = text.split("/")
    if len(splitted) == 2:
        if len(splitted[0]) == 7 and len(splitted[1]) == 5:
            if splitted[0].isdigit() and splitted[1].isdigit():
                return True
    else:
        return False

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
