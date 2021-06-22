import json
import uuid
import sqlite3
import sys
from typing import List, Optional

from goet.lib.converter.converter import converter
from goet.lib.frame.frame import Frame
from goet.tracer.base import BaseTracer

CURR_FRAME_ID: int = 0
PREV_FRAME_IDS: List[Optional[int]] = [None]


class SqlTracer(BaseTracer):
    """SqlTracer is used to record Python runtime.

    >>> with SqlTracer.trace_manager() as t:
    ...     fn()
    """

    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.run_id = str(uuid.uuid4())

    def __exit__(self, *exc):
        sys.settrace(None)
        val = super().__exit__(*exc)
        self.connection.commit()
        return val

    def dispatch_call(self, frame):
        PREV_FRAME_IDS.append(CURR_FRAME_ID)

    def dispatch_line(self, sysframe):
        with self.pause_tracing():
            global CURR_FRAME_ID
            CURR_FRAME_ID += 1

            frame = Frame.from_sysframe(sysframe, CURR_FRAME_ID, PREV_FRAME_IDS[-1])

            sql = f"""
            INSERT INTO frames (run_id, f_id, f_back_id, f_filename, f_lineno, f_locals)
            VALUES (?, ?, ?, ?, ?, ?)
            """
            args = (
                self.run_id,
                frame.f_id,
                frame.f_back_id,
                frame.f_filename,
                frame.f_lineno,
                json.dumps(converter.unstructure(frame.f_locals)),
            )
            self.cursor.execute(sql, args)

            sys.settrace(self.tracefunc)

    def dispatch_return(self, frame):
        PREV_FRAME_IDS.pop()

    def dispatch_exception(self, frame):
        pass

    def dispatch_opcode(self, frame):
        pass
