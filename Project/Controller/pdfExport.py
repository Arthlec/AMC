import os
import sys

import Controller.readAMC as ReadAMC


class PDFExport:
    def __init__(self):
        # Loads the data

        allQuestions, allStudents = ReadAMC.getStudentsAndQuestions()
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
                rawMdContent += '### Question {0} : {1}\n\n'.format(i, allQuestions[i].title)
                for j in range(len(allQuestions[i].answers)):
                    # print('j: ', j)
                    good = student.questions[i][j] == allQuestions[i].answers[j]
                    color = 'green' if good else 'red'
                    # code = '&#2713;' if good else '&#2717;'
                    code = u'✓' if good else u'✗'
                    checkbox = '[x]' if student.questions[i][j] else '[ ]'
                    rawMdContent += '- {0} <span style="color:{1}">{2} Choice {3}</span>\n'.format(checkbox, color, code, j)

                rawMdContent += '\n'

            f = open('{0}/{1}_{2}.md'.format(tempDir, student.id, student.name), 'w', encoding='utf-8')
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
