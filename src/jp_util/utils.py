# src/common_utils/utils.py
def common_function(x, y):
    return x + y

class CommonClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"