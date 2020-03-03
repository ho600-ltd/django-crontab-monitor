import threading



class CrontabJob(threading.Thread):
    def __init__(self, execute, args, kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()

        self.execute = execute
        self.args = args
        self.kwargs = kwargs
        

    def run(self):
        self.execute(*self.args, **self.kwargs)


