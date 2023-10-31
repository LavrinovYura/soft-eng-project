import sqlite3

class DataBase:

    def __init__(self, database_file):
        """Подключение к БД и сохранение курсора"""
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def user_exists(self, user_id):
        """Проверка есть ли пользователь в базе"""
        with self.connection:
            self.cursor.execute("SELECT * FROM usersInfo WHERE user_id = (?)", (user_id,))
            return bool(self.cursor.fetchall())

    def add_user(self, user_id):
        """Добавление нового пользователя"""
        self.cursor.execute("""INSERT INTO usersInfo (user_id) VALUES (?)""", (user_id,))
        return self.connection.commit()

    def set_group_id(self, user_id, group_id: str):
        """Установка номера группы пользователя"""
        self.cursor.execute(f"UPDATE usersInfo SET group_id = {group_id} WHERE user_id = {user_id}")
        return self.connection.commit()

    def get_group_id(self,user_id):
        """Получение номера группы"""
        group_id = self.cursor.execute("""SELECT group_id FROM usersInfo WHERE user_id = ?""", (user_id,)).fetchone()
        return group_id

    def close(self):
        """Закрытие соединения с БД"""
        self.connection.close()