import sqlite3
import sys

from goet.lib.frame.frame import Frame
from goet.lib.db.sqlite import connection
from goet.tracer.base import BaseTracer


class SqlTracer(BaseTracer):
    """SqlTracer is used to record Python runtime.

    >>> with SqlTracer.trace_manager() as t:
    ...     fn()
    """
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def __exit__(self, *exc):
        sys.settrace(None)
        val = super().__exit__(*exc)
        self.connection.commit()
        return val

    def dispatch_call(self, frame):
        pass

    def dispatch_line(self, sysframe):
        sys.settrace(None)
        frame = Frame.from_sysframe(sysframe)

        sql = f"""
        INSERT INTO lines (snapshot)
        VALUES (?)
        """

        args = (frame.to_json(), )
        self.cursor.execute(sql, args)

        sys.settrace(self.tracefunc)

    def dispatch_return(self, frame):
        pass

    def dispatch_exception(self, frame):
        pass

    def dispatch_opcode(self, frame):
        pass
