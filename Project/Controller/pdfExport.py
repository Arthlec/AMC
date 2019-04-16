from jinja2 import Environment, PackageLoader, select_autoescape
import os, sys
import errno
from weasyprint import HTML, CSS

class PDFExport:
    def __init__(self, data):
        self.html = 'res/export_template/student.html'
        self.css = 'res/export_template/style.css'
        self.data = data
        env = Environment(
            loader=PackageLoader('res', 'export_template'),
            autoescape=select_autoescape(['html', 'xml'])
        )

        self.template = env.get_template('student.html')

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

        # PDF part
        if not os.path.exists(pdfDir):
            try:
                os.makedirs(pdfDir)
            except OSError as exc: # To prevent race condition
                if exc.errno != errno.EEXIST:
                    raise

        HTML(os.path.join(tempDir, filename)).write_pdf(os.path.join(pdfDir, filename))



if __name__ == '__main__':
    ex = PDFExport('')