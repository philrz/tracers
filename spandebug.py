import sys
import inspect
import linecache
import json

SYSDIG_DEVICE = '/dev/sysdig'

d = open(SYSDIG_DEVICE, 'w', 0)
tags = []
tracenum = 0

class SysdigTrace():
    def __enter__(self):
        global tracenum

        tracenum += 1
        sys.settrace(emit_markers)
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)

def emit_markers(frame, event, arg):

    global tracenum
    global d
    global tags

    prior = inspect.currentframe().f_back
    span = [ '>', tracenum ]
    e = [
          { 'file': prior.f_code.co_filename },
          { 'event': event }
        ]

    if event == "call":
        tags.append(prior.f_code.co_name + '()')
        e.append({ 'lineno': str(inspect.currentframe().f_back.f_lineno) })
        d.write(json.dumps(['>', tracenum] + [tags] + [e]))
    elif event == "return":
        e.append({ 'lineno': str(inspect.currentframe().f_back.f_lineno) })
        d.write(json.dumps(['<', tracenum] + [tags] + [e]))
        tags.pop()

    return emit_markers
