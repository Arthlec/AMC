#Parsing data (one function to compare student sheet / answer sheet)
import json
from pprint import pprint
import Controller.computeData

stdAnswers={}
exmAnswers={}
stdScore={}
def parseAnswers(fileName):
    with open(fileName) as f:
        data = json.load(f)
        f.close()
    return data

stdAnswers=parseAnswers('../Model/dataset1.json')
exmAnswers=parseAnswers('../Model/dataset3.json')

#pprint(stdAnswers)
i=0;
j=0;
k=0
for i in range(len(stdAnswers)):
  #print("-----------student_" + str(i))
  stdScore["student_" + str(i)] ={}
  result={}
  b=0
  m=0
  for j in range(len(stdAnswers["student_"+str(i)])):
     #print("*****question_" + str(j))
     for k in range(len(stdAnswers["student_"+str(i)]["question_"+str(j)])):
        #print(k, "=", stdAnswers["student_" + str(i)]["question_" + str(j)][str(k)])
        #print(k, " answer =", exmAnswers["question_" + str(j)][str(k)])
        stdAns=stdAnswers["student_" + str(i)]["question_" + str(j)][str(k)]
        exmAns=exmAnswers["question_" + str(j)]["items"][str(k)]
        b = exmAnswers["question_" + str(j)]["b"]
        m= exmAnswers["question_" + str(j)]["m"]
        result["question_" + str(j)]={}
        if(stdAns==exmAns):
            result["question_" + str(j)]["ans"] = True
        else:
            result["question_" + str(j)]["ans"] = False
        result["question_" + str(j)]["b"] = b
        result["question_" + str(j)]["m"] = m
     stdScore["student_" + str(i)]=result

# pprint(stdScore)
stdQuestionsPoints = Controller.computeData.computeQuestionsPoints(stdScore)
# pprint(stdQuestionsPoints)
stdFinalMark = Controller.computeData.computeFinalMark(stdQuestionsPoints, stdScore)
pprint(stdFinalMark)
