import sys
import json
from goet.lib.frame.frame import Frame
from goet.tracer.base import BaseTracer
from pprint import pprint

class PrintTracer(BaseTracer):
    """PrintTracer is used to record Python runtime.

    >>> with PrintTracer.trace_manager() as t:
    ...     fn()
    """
    def dispatch_call(self, frame):
        # print(f"dispatch_call: {frame=}")
        pass

    def dispatch_line(self, sysframe):
        sys.settrace(None)
        frame = Frame.from_sysframe(sysframe)

        pprint(json.loads(frame.to_json()), indent=4)
        
        sys.settrace(self.tracefunc)

    def dispatch_return(self, frame):
        # print(f"dispatch_return: {frame=}")
        pass

    def dispatch_exception(self, frame):
        # print(f"dispatch_exception: {frame=}")
        pass

    def dispatch_opcode(self, frame):
        # print(f"dispatch_opcode: {frame=}")
        pass
