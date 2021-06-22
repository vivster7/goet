import sqlite3
from pathlib import Path

from goet.lib.path.get_root_dir import get_root_dir

ROOT_DIR = get_root_dir(__file__)
DB_NAME = "test.rdb.sqlite3"
connection = sqlite3.connect(Path(ROOT_DIR / DB_NAME))


def seed_db():
    cursor = connection.cursor()

    # snapshot consists of all the frames + all the variables
    sql = """
    DROP TABLE IF EXISTS frames;

    CREATE TABLE frames (
        id INTEGER PRIMARY KEY,
        run_id TEXT NOT NULL,
        f_id INTEGER NOT NULL,
        f_back_id INTEGER,
        f_filename TEXT NOT NULL,
        f_lineno INTEGER NOT NULL,
        f_locals TEXT NOT NULL
    );
    """

    cursor.executescript(sql)


seed_db()
