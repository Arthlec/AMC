class Exam:
    def __init__(self):
        pass


class Student:
    def __init__(self, name, firstName, studentId):
        self.name = name
        self.firstName = firstName
        self.studentId = studentId



class Question:
    def __init__(self, nb, answers):
        self.number = nb
        self.answers = answers


class Answer:
    def __init__(self, content):
        self.content = content
