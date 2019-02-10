class Accident(Exception):

    def __init__(self, msg):
        self.msg = msg

    def msg_print(self):
        return self.msg
