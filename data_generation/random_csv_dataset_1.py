import csv
import random

question_number = 20
student_number = 100

def main():
    with open('dataset1.csv', 'w') as out:
        data_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data_writer.writerow(['studentID', 'questionId', 'answers'])

        for i in range(student_number):
            for j in range(question_number):
                # result = [str(randint(0, 1)) for k in range(4)]
                result = ';'.join(str(random.randint(0, 1)) for k in range(4))
                data_writer.writerow([str(i), str(j), result])


if __name__ == '__main__':
    main()
