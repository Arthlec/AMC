#Parsing data (one function to compare student sheet / answer sheet)
import json
from pandas.io.json import json_normalize
import random
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
from scipy import stats
from scipy.stats import t
from pprint import pprint
import Controller.computeData
stdAnswers={}
exmAnswers={}
stdScore={}
answers={}
def parseAnswers(fileName):
    with open(fileName) as f:
        data = json.load(f)
        f.close()
    return data

stdAnswers=parseAnswers('../Model/dataset1.json')
exmAnswers=parseAnswers('../Model/dataset6.json')

i=0;
j=0;
k=0

for i in range(len(stdAnswers)):
  stdScore["student_" + str(i)] ={}
  answers["student_" + str(i)] ={}
  result={}
  res={}
  b=0
  m=0
  #need to add more options
  for j in range(len(stdAnswers["student_"+str(i)])):
     #print("*****question_" + str(j))
     len1=len(stdAnswers["student_"+str(i)]["question_"+str(j)])
     exam = exmAnswers["questions"][str(j)]["answers"]
     correctAns = exam[0]["correct"]
     b = exam[0]["strategy"]["b"]
     m = exam[0]["strategy"]["m"]
     result["question_" + str(j)] = {}
     res["question_" + str(j)] = {}
     for k in range(len1):
        stdAns=stdAnswers["student_" + str(i)]["question_" + str(j)][str(k)]
        result["question_" + str(j)]["b"] = b
        result["question_" + str(j)]["m"] = m

        if stdAns=="1":
          if k==correctAns:
            result["question_" + str(j)]["ans"] = True
            res["question_" + str(j)]=True
        else:
            result["question_" + str(j)]["ans"] = False
            res["question_" + str(j)] = False

     stdScore["student_" + str(i)]=result
     answers["student_" + str(i)]=res


#report
df = pd.DataFrame.from_dict(answers, orient='columns')
data=pd.DataFrame(answers)
falseCount=[]
trueCount=[]
lbl=[]
for i in range(20):
    trueCount.append((data.T[data.T["question_"+str(i)] == True]).shape[0])
    falseCount.append((data.T[data.T["question_" + str(i)] == False]).shape[0])
    lbl.append("question_" + str(i))

y_pos = np.arange(20)
plt.bar(y_pos, trueCount)
plt.xticks(y_pos, lbl,fontsize=6,rotation = 90)
plt.ylabel('True Answers')
plt.title('total correct answers for each question')
plt.savefig('total correct answers for each question.png')
plt.show()


y_pos = np.arange(20)
plt.bar(y_pos, falseCount)
plt.xticks(y_pos, lbl,fontsize=6,rotation = 90)
plt.ylabel('False Answers')
plt.title('total wrong answers for each question')
plt.savefig('total wrone answers for each question.png')
plt.show()



plt.plot(lbl, trueCount, label='True',color='g')
plt.xticks(y_pos, lbl, rotation='vertical')
plt.plot(lbl, falseCount,label='False', color='orange')
plt.xticks(y_pos, lbl, rotation='vertical')
plt.xlabel('question anmes')
plt.ylabel('answers')
plt.legend(loc='upper left')
plt.title('total wrone/corect answers for each question ')
plt.show()
plt.savefig('total wrone/corect answers for each question.png')


pprint(stdScore)
stdQuestionsPoints = Controller.computeData.computeQuestionsPoints(stdScore)
pprint(stdQuestionsPoints)
stdFinalMark = Controller.computeData.computeFinalMark(stdQuestionsPoints, stdScore)
pprint(stdFinalMark)