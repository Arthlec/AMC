# Q1 = 1 AND Q3 = 0 IS -1

from enum import Enum

class KeyWords(Enum):
    AND = 'AND'
    OR = 'OR'
    EQUAL = '=='
    IS = 'IS'


class Tokenizer:
    def __init__(self):
        pass

    def isKeyword(self, word):
        return word in Keywords


class Logic:
    def __init__(self, command):
        self.command = command
        self.interpretCommand(self.command)
        self.tokenizer = Tokenizer()

    def interpretCommand(command):



if __name__ == '__main__':
    command = input('Enter a logic command:\n')
    logic = Logic(command)
