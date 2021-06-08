import sqlite3
from pathlib import Path

from goet.lib.path.get_root_dir import get_root_dir

ROOT_DIR = get_root_dir(__file__)
DB_NAME = 'test.rdb.sqlite3'
connection = sqlite3.connect(Path(ROOT_DIR / DB_NAME))


def seed_db():
    cursor = connection.cursor()

    # snapshot consists of all the frames + all the variables
    sql = """
    DROP TABLE IF EXISTS lines;

    CREATE TABLE lines (
        id INTEGER PRIMARY KEY,
        snapshot BLOB
    );
    """

    cursor.executescript(sql)

seed_db()