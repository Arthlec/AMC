# Code about the logic implementation in the projectself.
# This section defines the keyword used in that new language as well
# as the syntax for the interpreter.
# Writer: Evrard CALLOT

# Example:
# Q1 = 1 AND Q3 = 0 IS -1

from enum import Enum
import nltk

class _KeyWords(Enum):
    AND = 'AND'
    OR = 'OR'
    EQUAL = '=='
    IS = 'IS'

class _QuestionResult:
    def __init__(self, id, res):
        self.id = id
        self.result = res

    def _printElement(self):
        return "QuestionResult {id: " + str(self.id) + ", result: " + str(self.result) + "}"

    def __repr__(self):
        return self._printElement()

    def __str__(self):
        return self._printElement()


class _LogicElement:
    def __init__(self, questions, ops, malus):
        self.questions = questions
        self.ops = ops
        self.malus = malus


class Logic:
    def __init__(self, command):
        self.command = command
        self.interpretCommand()

    def interpretCommand(self):
        tokens = self.command.split(' ')
        # tokens = nltk.word_tokenize(self.command)
        self.checkSyntaxErrors(tokens)
        firstRes = []
        n = len(tokens)
        for i in range(n):
            if tokens[i] == _KeyWords.EQUAL.value:
                firstRes.append(_QuestionResult(id=tokens[i - 1], res=tokens[i + 1]))
            if tokens[i] in [_KeyWords.AND.value, _KeyWords.OR.value]:
                firstRes.append(tokens[i])
            if tokens[i] == _KeyWords.IS.value:
                self.result = int(tokens[i + 1])

        print('PASS !')

    def checkSyntaxErrors(self, tokens):
        containIS = False
        n = len(tokens)
        keywords = [item.value for item in _KeyWords]

        for i in range(n):
            token = tokens[i]

            # Searches for the Keyword IS
            containIS = containIS or token == _KeyWords.IS.value

            # Checks if a Question statement is correctly written
            if token[0] == 'Q':
                try:
                    int(token[1:])
                except ValueError:
                    raise ValueError('The question should have a valid id for "' + token + '" in : ' + self.command)
                if len(token) == 1:
                    raise SyntaxError('The question should be followed by its ID in : ' + self.command)

                if tokens[i + 1] != _KeyWords.EQUAL.value:
                    raise SyntaxError('Missing statement "' + _KeyWords.EQUAL.value + '" after token "' + token + '" in : ' + self.command)

                if not self.is_digit(tokens[i + 2]):
                    raise SyntaxError('Missing value for question "' + token + '" in : ' + self.command)


            # If the token is a keyword
            elif token in keywords:
                if i == n - 1:
                    raise SyntaxError('Missing statement after "' + token + '" keyword in : ' + self.command)
                if i == 0:
                    raise SyntaxError('Missing statement before "' + token + '" keyword in : ' + self.command)
                nextToken = tokens[i + 1]

                if token in [_KeyWords.AND.value, _KeyWords.OR.value]:
                    if nextToken[0] != 'Q':
                        raise SyntaxError('Keyword "' + token + '" must be followed by a question statement in : ' + self.command)

                elif token == _KeyWords.IS.value:
                    if i != n - 2:
                        raise SyntaxError('"' + _KeyWords.IS.value + '" keyword should be the last statement in : ' + self.command)

                    if not self.is_digit(nextToken):
                        raise SyntaxError('Keyword "' + _KeyWords.IS.value + '" must be followed by an interger in : ' + self.command)


            # If the token is a digit, it must be
            elif self.is_digit(token) and i != n - 1 and tokens[i + 1][0] == 'Q':
                raise SyntaxError('Missing keyword in : ' + self.command)

            # If the token is not a digit, not a keyword and is not a question
            elif not self.is_digit(token):
                raise SyntaxError('Undefined keyword "' + token + '" in : ' + self.command)

        # If there is no IS keyword in the command
        if not containIS:
            raise SyntaxError('Missing keyword : "' + _KeyWords.IS.value + '" at "' + self.command + '".')


    def printLogic(self):
        return self.command

    def is_digit(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False



if __name__ == '__main__':
    command = input('Enter a logic command:\n')
    logic = Logic(command)
    # logic = Logic('Q1 == 1 AND Q2 == 0')
    # logic = Logic('Q1 == 1 AND Q2 IS 0')
    # logic = Logic('Q1 == 1 AND Q2 == 0 IS -2')
    # logic = Logic('Q1 == 1 AND Q2 == 0 IS 0')
    print(logic.printLogic())