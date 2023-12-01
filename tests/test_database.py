import unittest
import sqlite3
from src.db.database import Database

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.cursor = self.connection.cursor()
        self.database = Database(":memory:")
        self.database.connection = self.connection
        self.database.cursor = self.cursor

    def test_user_exists_existing_user(self):
        self.cursor.execute("CREATE TABLE usersInfo (user_id INTEGER)")
        self.cursor.execute("INSERT INTO usersInfo (user_id) VALUES (123)")
        self.assertTrue(self.database.user_exists(123))

    def test_user_exists_non_existing_user(self):
        self.cursor.execute("CREATE TABLE usersInfo (user_id INTEGER)")
        self.assertFalse(self.database.user_exists(123))

    def test_add_user(self):
        self.cursor.execute("CREATE TABLE usersInfo (user_id INTEGER)")
        self.database.add_user(123)
        self.cursor.execute("SELECT * FROM usersInfo WHERE user_id = 123")
        result = self.cursor.fetchone()
        self.assertIsNotNone(result)
        
    def test_get_group_id(self):
        self.cursor.execute("CREATE TABLE usersInfo (user_id INTEGER, group_id TEXT)")
        self.cursor.execute("INSERT INTO usersInfo (user_id, group_id) VALUES (123, 'AB123')")
        group_id = self.database.get_group_id(123)
        self.assertEqual(group_id[0], "AB123")

    def test_get_group_id_non_existing_user(self):
        self.cursor.execute("CREATE TABLE usersInfo (user_id INTEGER, group_id TEXT)")
        group_id = self.database.get_group_id(123)
        self.assertIsNone(group_id)

    def tearDown(self):
        self.connection.close()

if __name__ == '__main__':
    unittest.main()