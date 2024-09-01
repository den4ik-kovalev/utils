import sqlite3

import jsonpickle

import config
from library.sqlite import SQLite


def setup_custom_types() -> type:
    """ Пользовательские типы данных для сохранения в БД """

    from melody import Melody

    def adapt_pyobject(obj: object) -> bytes:
        return jsonpickle.encode(obj)

    def convert_pyobject(s: bytes) -> object:
        return jsonpickle.decode(s)

    sqlite3.register_adapter(Melody, adapt_pyobject)
    sqlite3.register_converter("PYOBJECT", convert_pyobject)

    return Melody


Melody = setup_custom_types()


class Database(SQLite):

    def insert_melody(self, name: str, melody: Melody) -> int:
        """ Добавить запись в таблицу melody """

        with self.connection() as conn:
            stmt = """
               INSERT INTO melody(name, obj, length, duration, grid_size) 
               VALUES (?, ?, ?, ?, ?)
               """
            values = (name, melody, melody.length, melody.duration.quarterLength, melody.grid_size)
            conn.execute(stmt, values)

            stmt = "SELECT last_insert_rowid() AS rowid"
            cur = conn.execute(stmt)
            return cur.fetchone()["rowid"]

    def select_melody(self, rowid: int) -> list[dict]:
        """ Получить одну запись из melody """

        with self.connection() as conn:
            stmt = "SELECT * FROM melody WHERE rowid = ?"
            cur = conn.execute(stmt, (rowid,))
            return cur.fetchone()

    def switch_melody_favorite(self, rowid: int):
        """ Поменять значение melody.favorite на противоположное """

        with self.connection() as conn:
            stmt = "UPDATE melody SET favorite = NOT favorite WHERE rowid = ?"
            conn.execute(stmt, (rowid,))

    def delete_melody(self, rowid: int):
        """ Удалить запись из melody """

        with self.connection() as conn:
            stmt = "DELETE FROM melody WHERE rowid = ?"
            conn.execute(stmt, (rowid,))


# запрос для инициализации таблиц БД
INIT_STMT = """
CREATE TABLE IF NOT EXISTS melody (
    name TEXT,
    obj PYOBJECT,
    length INT,
    duration REAL,
    grid_size REAL,
    favorite INT DEFAULT 0
)
"""

db = Database(
    filepath=(config.app_dir / "main.db"),
    init_stmt=INIT_STMT
)
