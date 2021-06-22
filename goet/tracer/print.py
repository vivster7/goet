import sys
import json
from typing import List, Optional
from goet.lib.converter.converter import converter
from goet.lib.frame.frame import Frame
from goet.tracer.base import BaseTracer
from pprint import pprint

CURR_FRAME_ID: int = 0
PREV_FRAME_IDS: List[Optional[int]] = [None]


class PrintTracer(BaseTracer):
    """PrintTracer is used to record Python runtime.

    >>> with PrintTracer.trace_manager() as t:
    ...     fn()

    line():
     - increment frame_id

    call():
     - add curr_frame to prev_frame_id

    return():
     - update prev_frame_id

    increment frame_id:
      - call()
      - line()

    0 1 1 3 1 1
    1 2 3 4 5 6

          x
      x x x x x
    x x x x x x
    """

    def dispatch_call(self, frame):
        PREV_FRAME_IDS.append(CURR_FRAME_ID)
        # print(f"dispatch_call: {frame=}")

    def dispatch_line(self, sysframe):
        # print(f"dispatch_line: {sysframe=}")

        with self.pause_tracing():
            global CURR_FRAME_ID
            CURR_FRAME_ID += 1
            frame = Frame.from_sysframe(sysframe, CURR_FRAME_ID, PREV_FRAME_IDS[-1])
            pprint(converter.unstructure(frame), indent=4)

    def dispatch_return(self, frame):
        PREV_FRAME_IDS.pop()
        # print(f"dispatch_return: {frame=}")

    def dispatch_exception(self, frame):
        # print(f"dispatch_exception: {frame=}")
        pass

    def dispatch_opcode(self, frame):
        # print(f"dispatch_opcode: {frame=}")
        pass
