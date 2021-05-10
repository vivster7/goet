import sqlite3
import sys
import cattr
from cattr.preconf.json import make_converter
import json
from sqlite3.dbapi2 import connect

from goet.frame import Frame
from goet.tracer.base import BaseTracer

connection = sqlite3.connect('test.rdb.sqlite3')
cursor = connection.cursor()


# snapshot consists of all the frames + all the variables
sql = '''
DROP TABLE IF EXISTS lines;

CREATE TABLE lines (
    id INTEGER PRIMARY KEY,
    snapshot BLOB
);
'''

cursor.executescript(sql)


class SqlTracer(BaseTracer):
    """SqlTracer is used to record Python runtime.

    >>> with SqlTracer.trace_manager() as t:
    ...     fn()
    """
    def dispatch_call(self, frame):
        pass

    def dispatch_line(self, sysframe):
        sys.settrace(None)
        frame = Frame.from_sysframe(sysframe)
        
        sql = f'''
        INSERT INTO lines (id, snapshot)
        VALUES (?, ?)
        '''
        
        args = (frame.f_lineno, frame.to_json())
        cursor.execute(sql, args)

        sys.settrace(self.tracefunc)

    def dispatch_return(self, frame):
        pass

    def dispatch_exception(self, frame):
        pass

    def dispatch_opcode(self, frame):
        pass
