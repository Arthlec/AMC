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
        param = {} # parameters

        for k in range(random.randint(1, 6)):
            result[k] = str(random.randint(0, 1))

        param["e"] = 0 # non-coherent answer (multiple answer whereas simple solution)
        param["v"] = 0 # no box is checked
        param["d"] = 0 # offset for all non-e non-v cases
        param["p"] = 0 # default score (the floor) given for any score below or equal to p
        param["b"] = random.randint(1,3) # points given for a good answer
        param["m"] = -random.randint(1,3) # negative points given for a bad answer
        # param["auto"] = 2 # points used in an indicative question (special case we don't use)
        param["mz"] = 0 # points given for a good answer in a strict question (all good answers or nothing)
        param["haut"] = 0 # points given for a good answer and -1 per bad answer
        # param["MAX"] = 0 # max of points (not needed if it is the same value as the sum of good answers)
        # param["formula"] = 0 # useful if a formula is needed (not our case and it makes it simpler to use the other variables)

        data[question_id]["items"]=result
        data[question_id]["param"]=param
    # Once the data is generated, we save it in a file 'dataset.json' with
    # indentation so that the result is readable for a human
    with open('dataset4.json', 'w') as out:
        json.dump(data, out, indent=2)

if __name__ == '__main__':
    main2()
