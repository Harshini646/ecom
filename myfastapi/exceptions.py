class CustomException(Exception):
    def __init__(self, name, message):
        self.name = name
        self.message = message
        super().__init__(self.message)
