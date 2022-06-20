class Logger:

    def __init__(self):
        pass

    def log(self, msg):
        self.out_file = open("logs", "a+")
        self.out_file.write(str(repr(msg)) + '\n')
        self.out_file.close()
