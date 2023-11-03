from datetime import timedelta, timezone, datetime

import requests
from bs4 import BeautifulSoup

months = ["янв", "февр", "мар", "апр", "мая", "июня", "июля", "авг", "сент", "окт", "нояб", "дек"]


def get_url_with_schedule(group):
    link = f'https://ruz.spbstu.ru/search/groups?q={group.split("/")[0]}%2F{group.split("/")[1]}'
    data = requests.get(link).text
    soup = BeautifulSoup(data, 'html.parser')
    return "https://ruz.spbstu.ru" + soup.find("a", {"class": "groups-list__link"})['href']


def get_schedule(group):
    link = get_url_with_schedule(group)
    data = requests.get(link).text
    soup = BeautifulSoup(data, 'html.parser')
    schedule = soup.find("ul", class_="schedule").find_all("li", class_="schedule__day")
    result = ''
    for day in schedule:
        date = day.find(class_="schedule__date").text
        res_lessons = ''
        for lesson in day.find_all(class_="lesson"):
            lesson_subject = lesson.find(class_="lesson__subject").text
            lesson_place = lesson.find(class_="lesson__places").text
            res_lessons += f'\n{lesson_subject}\n{lesson_place}\n'
        result += f'\n<b>{date}</b>' + res_lessons
    return result.strip()


def get_today_schedule(group):
    link = get_url_with_schedule(group)
    data = requests.get(link).text
    soup = BeautifulSoup(data, 'html.parser')
    schedule = soup.find("ul", class_="schedule").find_all("li", class_="schedule__day")
    result = 'Сегодня занятий нет!'
    res_lessons = ''
    date = ''
    for day in schedule:
        date = day.find(class_="schedule__date").text[:-5]
        if date == get_date():
            for lesson in day.find_all(class_="lesson"):
                lesson_subject = lesson.find(class_="lesson__subject").text
                lesson_place = lesson.find(class_="lesson__places").text
                res_lessons += f'\n{lesson_subject}\n{lesson_place}\n'
    if res_lessons != '':
        result = f'\n<b>{get_date()}</b>' + res_lessons
    return result


def get_date():
    offset = timedelta(hours=3)
    tz = timezone(offset)
    return datetime.now(tz).strftime("%d") + " " + months[int(datetime.now(tz).strftime("%m")) - 1]