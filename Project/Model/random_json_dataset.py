import json
import random
import numpy as np
question_number = 20
student_number = 100

def main():
    # The data variable will hold the final dataset and to be saved later
    data = {}

    # For each student
    for i in range(student_number):
        # We generate a student id (for example: student_12)
        student_id ='student_' + str(i)
        # This student will hold a structure. This will be all
        # his answers
        data[student_id] = {}

        # For each question
        for j in range(question_number):
            # We generate a question id (for example: question_5)
            question_id = 'question_' + str(j)

            # The result variable will hold the answers of the student
            # for that question. This is formaated as a string like 0;0;1;0
           # result=[str(random.randint(0, 1)) for k in range(4)]
            result ={}# ';'.join(str(random.randint(0, 1)) for k in range(4))
            for k in range(4):
                result[k] = str(random.randint(0, 1))
            data[student_id][question_id]=result
    # Once the data is generated, we save it in a file 'dataset.json' with
    # indentation so that the result is readable for a human
    with open('dataset1.json', 'w') as out:
        json.dump(data, out, indent=2)


def main2():
    # The data variable will hold the final dataset and to be saved later
    data = {}

    # For each student
    for i in range(question_number):
        # We generate a student id (for example: student_12)
        question_id ='question_' + str(i)
        # This student will hold a structure. This will be all
        # his answers
        data[question_id] = {}
        # For each question
        result ={}# ';'.join(str(random.randint(0, 1)) for k in range(4))
        for k in range(4):
            result[k] = str(random.randint(0, 1))

        data[question_id]["items"]=result
        data[question_id]["b"] = 2
        data[question_id]["m"] = -1
    # Once the data is generated, we save it in a file 'dataset.json' with
    # indentation so that the result is readable for a human
    with open('dataset3.json', 'w') as out:
        json.dump(data, out, indent=2)

if __name__ == '__main__':
    main2()
