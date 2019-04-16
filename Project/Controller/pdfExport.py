from jinja2 import Environment, PackageLoader, select_autoescape
import os, sys
import errno
import Controller.readAMC as ReadAMC
# from weasyprint import HTML, CSS

class _Question():
    def __init__(self, id=None, title=''):
        self.id = id
        self.title = title
        self.answers = {}

    def addAnswer(self, answerId, correct):
        self.answers[str(answerId)] = correct

    def defined(self, answerId):
        return str(answerId) in self.answers


class _Student():
    def __init__(self, id=None, name=''):
        self.id = id
        self.name = name
        self.questions = {}

    def addAnswer(self, questionId, answerId, ticked):
        id = str(questionId)

        if id not in self.questions:
            self.questions[id] = {}

        self.questions[id][str(answerId)] = ticked



class PDFExport:
    def __init__(self):
        # Loads the template
        self.html = 'res/export_template/student.html'
        self.css = 'res/export_template/style.css'
        # self.data = data
        env = Environment(
            loader=PackageLoader('res', 'export_template'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        self.template = env.get_template('student.html')

        # Loads the data
        boxes, resultatsPoints = ReadAMC.updateData()
        print(boxes)

        allStudents = []
        allQuestions = {}

        studentId = -1
        student = None
        for index, row in boxes.iterrows():
            questionId = str(row['question'])

            if row['student'] != studentId:
                if student is not None:
                    allStudents.append(student)
                studentId = row['student']
                student = _Student(id=studentId)

            student.addAnswer(row['question'], row['answer'], row['ticked'])

            if questionId not in allQuestions:
                allQuestions[questionId] = _Question(id=row['question'])

            if not allQuestions[questionId].defined(row['answer']):
                allQuestions[questionId].addAnswer(row['answer'], row['correct'])

        print(allStudents)
        print(allQuestions)


    def export(self):
        rootDir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        tempDir = os.path.join(rootDir, 'output/temp')
        pdfDir = os.path.join(rootDir, 'output/examTest')

        filename = 'studentTest.html'


        render = self.template.render(self.data)

        # HTML part
        f = open(os.path.join(tempDir, filename), 'w')
        f.write(render)
        f.close()

        # # PDF part
        # if not os.path.exists(pdfDir):
        #     try:
        #         os.makedirs(pdfDir)
        #     except OSError as exc: # To prevent race condition
        #         if exc.errno != errno.EEXIST:
        #             raise
        #
        # HTML(os.path.join(tempDir, filename)).write_pdf(os.path.join(pdfDir, filename))



if __name__ == '__main__':
    ex = PDFExport('')
