import json
import random

question_number = 20
student_number = 100

def main():
    data = {}

    for i in range(student_number):
        student_id = 'student_' + str(i)
        data[student_id] = {}
        for j in range(question_number):
            question_id = 'question_' + str(j)
            result = ';'.join(str(random.randint(0, 1)) for k in range(4))
            data[student_id][question_id] = result

    with open('dataset.json', 'w') as out:
        json.dump(data, out, indent=2)

if __name__ == '__main__':
    main()
