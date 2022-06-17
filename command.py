class Command():
    def __init__(self, name, exec, log=True, alias=[]):
        self.name = name
        self.exec = exec
        self.log = log
        self.alias = alias

    def execute(self, msg):
        if(log):
            print("Command used: {self.name} by user:")
        self.exec(msg)