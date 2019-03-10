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
    for p in range(1):      #student_number in the final version
        data["main_strategy"] = ""
        data["questions"] = {}
        for i in range(question_number):
            question_id ='question_' + str(i)
            data["questions"][i] = {}
            data["questions"][i]["question"] = i
            data["questions"][i]["questionID"] = question_id
            data["questions"][i]["type"] = 1
            data["questions"][i]["indicative"] = 0
            data["questions"][i]["strategy"] = ""

            numberOfAnswers = random.randint(2,6) # number of answers in the question
            data["questions"][i]["answers"] = []

            for k in range(1):#numberOfAnswers):
                answer = {}
                answer["question"] = i
                answer["answer"] = k
                answer["correct"] = random.randint(0,3)
                answer["ticked"] = random.randint(0,3)

                strategyForChoices = {}
                strategyForChoices["e"] = 0 # non-coherent answer (multiple answer whereas simple solution)
                strategyForChoices["v"] = 0 # no box is checked
                strategyForChoices["d"] = 0 # offset for all non-e non-v cases
                strategyForChoices["p"] = 0 # default score (the floor) given for any score below or equal to p
                strategyForChoices["b"] = random.randint(1,3) # points given for a good answer
                strategyForChoices["m"] = -random.randint(1,3) # negative points given for a bad answer
                # strategyForChoices["auto"] = 2 # points used in an indicative question (special case we don't use)
                strategyForChoices["mz"] = 0 # points given for a good answer in a strict question (all good answers or nothing)
                strategyForChoices["haut"] = 0 # points given for a good answer and -1 per bad answer
                # strategyForChoices["MAX"] = 0 # max of points (not needed if it is the same value as the sum of good answers)
                # strategyForChoices["formula"] = 0 # useful if a formula is needed (not our case and it makes it simpler to use the other variables)

                answer["strategy"] = strategyForChoices
                data["questions"][i]["answers"].append(answer)



    # Once the data is generated, we save it in a file 'dataset.json' with
    # indentation so that the result is readable for a human
    with open('dataset6.json', 'w') as out:
        json.dump(data, out, indent=2)

if __name__ == '__main__':
    main2()
