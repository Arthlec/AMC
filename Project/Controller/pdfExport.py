import os
import sys

import Controller.readAMC as ReadAMC


class PDFExport:
    def __init__(self):
        # Loads the data

        self.allQuestions, self.allStudents = ReadAMC.getStudentsAndQuestions()
        self.date = ReadAMC.examDate


    def export(self):
        rootDir = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))
        outDir = os.path.join(rootDir, 'output/exam_{0}'.format(self.date.replace('/', '_')))

        self.createDir(outDir)

        for studentKey, student in self.allStudents.items():
            rawMdContent = 'StudentID : {0}\nStudent Name : {1}\n<span style="color:red">Score : {2} / 20</span>\n\n'.format(student.id, student.name, student.globalResult)
            rawMdContent += '# Correction of the exam of {0}\n\n'.format(self.date)

            for i in range(1, len(self.allQuestions) + 1):
                # print("i: ", i)
                rawMdContent += '### Question {0} : {1}\n\n'.format(i, self.allQuestions[i].title)
                for j in range(len(self.allQuestions[i].answers)):
                    # print('j: ', j)
                    good = student.questions[i][j] == self.allQuestions[i].answers[j]
                    color = 'green' if good else 'red'
                    # code = '&#2713;' if good else '&#2717;'
                    code = u'✓' if good else u'✗'
                    checkbox = '[x]' if student.questions[i][j] else '[ ]'
                    rawMdContent += '- {0} <span style="color:{1}">{2} Choice {3}</span>\n'.format(checkbox, color, code, j + 1)

                rawMdContent += '\n'

            f = open('{0}/{1}_{2}.md'.format(outDir, student.id, student.name), 'w', encoding='utf-8')
            f.write(rawMdContent)
            f.close()

    def createDir(self, dir):
        if not os.path.exists(dir):
            os.makedirs(dir)




if __name__ == '__main__':
    ex = PDFExport('')
