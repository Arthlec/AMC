# Code about the logic implementation in the projectself.
# This section defines the keyword used in that new language as well
# as the syntax for the interpreter.
# Writer: Evrard CALLOT

# Example:
# Q1 = 1 AND Q3 = 0 IS -1

from enum import Enum
import nltk

class KeyWords(Enum):
    AND = 'AND'
    OR = 'OR'
    EQUAL = '=='
    IS = 'IS'

class QuestionResult:
    def __init__(self, id, res):
        self.id = id
        self.result = result


class LogicElement:
    def __init__(self, questions, ops, malus):
        self.questions = questions
        self.ops = ops
        self.malus = malus


class Logic:
    def __init__(self, command):
        self.command = command
        self.interpretCommand(self.command)

    def interpretCommand(self, command):
        tokens = nltk.word_tokenize(command)
        self.checkSyntaxErrors(tokens)
        n = len(tokens)
        for i in range(n):
            if tokens[i] == KeyWords.EQUAL:
                


    def checkSyntaxErrors(self, tokens):
        pass

    def writeLogic(self):
        return ''



if __name__ == '__main__':
    command = input('Enter a logic command:\n')
    logic = Logic(command)
    print(logic.writeLogic())
