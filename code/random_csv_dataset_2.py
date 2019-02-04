import csv
import random

question_number = 20
student_number = 100

def main():
    with open('dataset2.csv', 'w') as out:
        data_writer = csv.writer(out, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        data_writer.writerow(['studentID', 'answers'])

        for i in range(student_number):
            answers = []
            for j in range(question_number):
                # result = [str(randint(0, 1)) for k in range(4)]
                result = ';'.join(str(random.randint(0, 1)) for k in range(4))
                answers.append(result)

            data_writer.writerow([str(i)] + answers)




if __name__ == '__main__':
    main()
