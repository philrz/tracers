import sys
import inspect
import json

SYSDIG_DEVICE = '/dev/sysdig'

tracenum = 0     # Use "t" instead when Tracers support this in JSON

class SysdigTrace():
    def __enter__(self):
        global tracenum

        tracenum += 1
        self.tnum = tracenum
        self.d = open(SYSDIG_DEVICE, 'w', 0)
        self.tags = []
        sys.settrace(self.emit_markers)

        return self

    def emit_markers(self, frame, event, arg):
    
        prior = inspect.currentframe().f_back
        span = [ '>', self.tnum ]
        e = [
              { 'file': prior.f_code.co_filename },
              { 'event': event }
            ]
    
        if event == "call":
            self.tags.append(prior.f_code.co_name + '()')
            e.append({ 'lineno': str(inspect.currentframe().f_back.f_lineno) })
            self.d.write(json.dumps(['>', self.tnum] + [self.tags] + [e]))
        elif event == "return":
            e.append({ 'lineno': str(inspect.currentframe().f_back.f_lineno) })
            self.d.write(json.dumps(['<', self.tnum] + [self.tags] + [e]))
            self.tags.pop()
    
        return self.emit_markers

    def __exit__(self, ext_type, exc_value, traceback):
        sys.settrace(None)
        self.d.close()

