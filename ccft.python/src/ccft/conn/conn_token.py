class Token:
    flag: bool

    def __init__(self):
        self.flag = True

    def Cancel(self):
        self.flag = False

    def Status(self):
        return self.flag
