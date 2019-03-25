# Logic package

The logic package implement the analysis of a logic-based language for Multiple Choice Questions exams.

This is implemented in order to avoid student answering questions randomly and having nonsensical answers.

```
Q1 == 1 AND Q2 == 0 IS -2
R2 == 1 OR R3 == 1 IS -1
```

Which means that if a student was right for the question 1, but was not for question 2, he will get a malus of -2 points.



To use this, you need to import the module `Controller.Logic.logic`.
This module gives the user two things : the class `Logic` and the enum `LogicElement`. 

For example :

```python
import Controller.Logic.logic

def main():
    command = input('Enter a logic command for your questions:\n')
    logicQ = Logic(command, LogicElement.Q)
    command = input('Enter a logic command for your answers:\n')
    logicR = Logic(command, LogicElement.R)

    # TODO: Implement the check result part
    newResults = logic.checkResults(oldResults)
```

The `Logic` constructor takes as parameters : 

* A `string` as the command to parse. => default : `""`
* A `LogicElement` member, to tell the logic if it analyses questions or answers => default : `LogicElement.Q`

You can later give the `Logic` object the full results of a student and it will adjust the final grade.

