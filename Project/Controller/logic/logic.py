# Code about the logic implementation in the projectself.
# This section defines the keyword used in that new language as well
# as the syntax for the interpreter.
# Writer: Evrard CALLOT

# Example:
# Q1 = 1 AND Q3 = 0 IS -1

from enum import Enum

### Enumeration of known keywords for the formula
class _KeyWords(Enum):
    AND = 'AND'
    OR = 'OR'
    XOR = 'XOR'
    EQUAL = '=='
    IS = 'IS'

### Associates a Question/Answer id with its result
class _Result:
    def __init__(self, id, res):
        self.id = id
        self.result = res

    def isCorrect(self, res):
        return self.result == res


### Enumeration of possible logical element. To distinguish
#   a question (Q) with a Response (R)
class LogicElement(Enum):
    Q = 'Q'
    R = 'R'

### Contains the formula typed by the teacher. This formula will
#   be analysed to detect any mistake. It will then be processed
#   to return a malus/bonus for a student
class Logic:
    ### Initialisation
    #   param: "command" (String) : the command typed by the teacher
    #   parma: "selectionToken" (LogicElement) : indicator for a Question or a Response
    def __init__(self, command="", selectionToken=LogicElement.Q):
        if not isinstance(selectionToken, LogicElement):
            raise AssertionError('The parameter selectionToken should be an instance of LogicElement')
        self.selectionToken = selectionToken.value
        self.command = command
        if command != "" :
            self.interpretCommand()

    ### Sets or modify the current command
    def setCommand(self, command=""):
        if command != "":
            self.command = command

    ### Will process the current command to transform it
    #   into logic values
    def interpretCommand(self):
        # Each token (word) must be separated by a ' ' character
        tokens = self.command.split(' ')

        self.checkSyntaxErrors(tokens)
        firstRes = []
        n = len(tokens)
        for i in range(n):
            if tokens[i] == _KeyWords.EQUAL.value:
                firstRes.append(_Result(id=tokens[i - 1], res=int(tokens[i + 1])))
            if tokens[i] in [_KeyWords.AND.value, _KeyWords.OR.value, _KeyWords.XOR.value]:
                firstRes.append(tokens[i])
            if tokens[i] == _KeyWords.IS.value:
                self.result = int(tokens[i + 1])

        self.tokens = firstRes
        print('PASS !')

    ### Checks for any syntax error in the command
    #   raise an Exception if a mistake is found
    def checkSyntaxErrors(self, tokens):
        containIS = False
        n = len(tokens)
        keywords = [item.value for item in _KeyWords]

        for i in range(n):
            token = tokens[i]

            # Searches for the Keyword IS
            containIS = containIS or token == _KeyWords.IS.value

            # Checks if a Question statement is correctly written
            if token[0] == self.selectionToken:
                try:
                    int(token[1:])
                except ValueError:
                    raise ValueError('The question should have a valid id for "' + token + '" in : ' + self.command)
                if len(token) == 1:
                    raise SyntaxError('The question should be followed by its ID in : ' + self.command)

                if tokens[i + 1] != _KeyWords.EQUAL.value:
                    raise SyntaxError('Missing statement "' + _KeyWords.EQUAL.value + '" after token "' + token + '" in : ' + self.command)

                if not self._is_digit(tokens[i + 2]):
                    raise SyntaxError('Missing value for question "' + token + '" in : ' + self.command)


            # If the token is a keyword
            elif token in keywords:
                if i == n - 1:
                    raise SyntaxError('Missing statement after "' + token + '" keyword in : ' + self.command)
                if i == 0:
                    raise SyntaxError('Missing statement before "' + token + '" keyword in : ' + self.command)
                nextToken = tokens[i + 1]

                if token in [_KeyWords.AND.value, _KeyWords.OR.value, _KeyWords.XOR.value]:
                    if nextToken[0] != self.selectionToken:
                        raise SyntaxError('Keyword "' + token + '" must be followed by a question statement in : ' + self.command)

                elif token == _KeyWords.IS.value:
                    if i != n - 2:
                        raise SyntaxError('"' + _KeyWords.IS.value + '" keyword should be the last statement in : ' + self.command)

                    if not self._is_digit(nextToken):
                        raise SyntaxError('Keyword "' + _KeyWords.IS.value + '" must be followed by an interger in : ' + self.command)


            # If the token is a digit
            elif self._is_digit(token) and i != n - 1 and tokens[i + 1][0] == self.selectionToken:
                raise SyntaxError('Missing keyword in : ' + self.command)

            # If the token is not a digit, not a keyword and is not a question
            elif not self._is_digit(token):
                raise SyntaxError('Undefined keyword "' + token + '" in : ' + self.command)

        # If there is no IS keyword in the command
        if not containIS:
            raise SyntaxError('Missing keyword : "' + _KeyWords.IS.value + '" at "' + self.command + '".')


    def printLogic(self):
        return self.command

    def _is_digit(self, value):
        try:
            int(value)
            return True
        except ValueError:
            return False

    # [(id, result)] correctedAnswers
    # id : the id of the question / answer
    # result : [0 or 1], if the question / answer is correct
    def checkResults(self, correctedAnswers):
        if self.result == '':
            raise ValueError('No command was specified for this Logic object...')

        isError = True
        results = [None] * len(correctedAnswers)
        errorArray = [None] * len(self.tokens)
        for id, res in correctedAnswers:
            results[id - 1] = res
        # print('Results: ', results)

        for i in range(len(self.tokens)):
            if isinstance(self.tokens[i], str):
                operator = self.tokens[i]
                firstRes = isError if i > 1 else self.tokens[i - 1].isCorrect(results[int(self.tokens[i - 1].id[1:]) - 1])
                secondRes = self.tokens[i + 1].isCorrect(results[int(self.tokens[i + 1].id[1:]) - 1])
                if operator == _KeyWords.AND.value:
                    isError = firstRes and secondRes
                elif operator == _KeyWords.OR.value:
                    isError = firstRes or secondRes
                elif operator == _KeyWords.XOR.value:
                    isError = (firstRes or secondRes) and not (firstRes and secondRes)
                else:
                    raise Error('Unknown operator: ' + token)

        return self.result if isError else 0



if __name__ == '__main__':
#     # command = input('Enter a logic command:\n')
#     # logic = Logic(command)
#     # logic = Logic('Q1 == 1 AND Q2 == 0')
#     # logic = Logic('Q1 == 1 AND Q2 IS 0')
#     # logic = Logic('Q1 == 1 AND Q2 == 0 IS -2')
    logic = Logic('R2 == 1 AND R3 == 0 IS -4', LogicElement.R)
    results = [(1, 1), (2, 1), (3, 0), (4, 1)]
    # results = [(1, 1), (2, 1), (3, 2)]
    newRes = logic.checkResults(results)
