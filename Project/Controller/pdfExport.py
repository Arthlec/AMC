import os, sys
import errno
import Controller.readAMC as ReadAMC

class _Question():
    def __init__(self, id=None, title=''):
        self.id = id
        self.title = title
        self.answers = {}

    def addAnswer(self, answerId, correct):
        self.answers[answerId] = correct

    def defined(self, answerId):
        return answerId in self.answers


class _Student():
    def __init__(self, id=None, name=''):
        self.id = id
        self.name = name
        self.questions = {}

    def addAnswer(self, questionId, answerId, ticked):
        if questionId not in self.questions:
            self.questions[questionId] = {}

        self.questions[questionId][answerId] = ticked



class PDFExport:
    def __init__(self):
        # Loads the data
        boxes, resultatsPoints = ReadAMC.updateData()
        print(boxes)

        allStudents = {}
        allQuestions = {}

        studentId = -1
        student = None
        for index, row in boxes.iterrows():
            questionId = row['question']
            studentId = row['student']

            if studentId not in allStudents:
                allStudents[studentId] = _Student(id=studentId)

            allStudents[studentId].addAnswer(row['question'], row['answer'], row['ticked'])

            if questionId not in allQuestions:
                allQuestions[questionId] = _Question(id=row['question'])

            if not allQuestions[questionId].defined(row['answer']):
                allQuestions[questionId].addAnswer(row['answer'], row['correct'])

        print(allStudents)
        print(allQuestions)
        self.export(allStudents, allQuestions)


    def export(self, allStudents, allQuestions):
        rootDir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        tempDir = os.path.join(rootDir, 'output/temp')
        pdfDir = os.path.join(rootDir, 'output/examTest')

        for studentKey, student in allStudents.items():
            rawMdContent = 'StudentID : {0}\nStudent Name : {1}\n\n'.format(student.id, student.name)
            rawMdContent += '# Correction of the exam of {0}\n\n'.format('02/01/2019')

            for i in range(1, len(allQuestions) + 1):
                # print("i: ", i)
                rawMdContent += '### Question {0}\n\n'.format(i)
                for j in range(1, len(allQuestions[i].answers)):
                    # print('j: ', j)
                    good = student.questions[i][j] == allQuestions[i].answers[j]
                    color = 'green' if good else 'red'
                    # code = '&#2713;' if good else '&#2717;'
                    code = u'✓' if good else u'✗'
                    checkbox = '[x]' if student.questions[i][j] else '[ ]'
                    rawMdContent += '- {0} <span style="color:{1}">{2} {3}</span>\n'.format(checkbox, color, code, '')

                rawMdContent += '\n'

            f = open('{0}/{1}.md'.format(tempDir, student.id), 'w', encoding='utf-8')
            f.write(rawMdContent)
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
