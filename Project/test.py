from Controller.pdfExport import PDFExport
from Controller.exam import Question, Answer


if __name__ == '__main__':
    data = {
        'date': '02/01/2019',
        'questions': [
            Question(1, [Answer('Choice 1'), Answer('Choice 2'), Answer('Choice 3'), Answer('Choice 4')]),
            Question(2, [Answer('Choice 1'), Answer('Choice 2'), Answer('Choice 3'), Answer('Choice 4')]),
            Question(3, [Answer('Choice 1'), Answer('Choice 2'), Answer('Choice 3'), Answer('Choice 4')]),
            Question(4, [Answer('Choice 1'), Answer('Choice 2'), Answer('Choice 3'), Answer('Choice 4')]),
        ]
    }
    ex = PDFExport(data)
    ex.export()
