#Parsing data (one function to compare student sheet / answer sheet)
import json
from pprint import pprint

stdAnswers={}
exmAnswers={}
stdScore={}
def parseAnswers(fileName):
    with open(fileName) as f:
        data = json.load(f)
        f.close()
    return data

stdAnswers=parseAnswers('../Model/dataset1.json')
exmAnswers=parseAnswers('../Model/dataset2.json')

#pprint(stdAnswers)
i=0;
j=0;
k=0
for i in range(len(stdAnswers)):
  #print("-----------student_" + str(i))
  stdScore["student_" + str(i)] ={}
  result={}
  for j in range(len(stdAnswers["student_"+str(i)])):
     #print("*****question_" + str(j))
     for k in range(len(stdAnswers["student_"+str(i)]["question_"+str(j)])):
        #print(k, "=", stdAnswers["student_" + str(i)]["question_" + str(j)][str(k)])
        #print(k, " answer =", exmAnswers["question_" + str(j)][str(k)])
        stdAns=stdAnswers["student_" + str(i)]["question_" + str(j)][str(k)]
        exmAns=exmAnswers["question_" + str(j)][str(k)]
        if(stdAns==exmAns):
            result["question_" + str(j)]= True
        else:
            result["question_" + str(j)]= False

     stdScore["student_" + str(i)]=result

pprint(stdScore)

#compare
