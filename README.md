# PolyNavi

Телеграм-бот для студентов

## Описание

Он предназначен для первокурсников - с ним освоиться в Политехе будет проще и интереснее. Наш бот предоставляет информацию о расписании пар, может отвечать на многие вопросы или перенаправить Ваш вопрос в Центр Качества Образования. Кроме того, в нем вы будете получать рассылку о самых важных новостях из жизни университета.

Этот репозиторий содержит исходный код и материалы для нашего проекта по программной инженерии. Проект разрабатывается в рамках обучения.

## Структура репозитория

- [/python](/python): в этой директории находится исходный код нашего проекта.
- [/tests](/tests): директория с тестами нашего кода.
- [/resources](/resources): в этой директории хранится база данных
- [.env](.env): настройки окружения проекта
## Как начать

1. Клонирование репозитория:
    
        git clone https://github.com/LavrinovYura/soft-eng-project.git
   
        cd soft-eng-project
    

3. Установка зависимостей:
    
        pip install -r requirements.txt

4. Измените содержимое .env используя ваши данные


5. Запуск проекта:
    
        python bot.py
    

6. Запуск тестов:
    
        python -m unittest tests/*

## Docker    
Чтобы развернуть бота в Docker-контейнере, используйте команды:

    docker-compose build

    docker-compose up
## Лицензия

Этот проект лицензирован в соответствии с условиями лицензии MIT — подробности см. в файле [LICENSE](LICENSE).
