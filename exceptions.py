# Custom exceptions\nclass CustomException(Exception):\n    def __init__(self, name, message):\n        self.name = name\n        self.message = message\n        super().__init__(self.message) 
