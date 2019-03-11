# Logic package

The logic package implement the analysis of a logic-based language for Multiple Choice Questions exams.

This is implemented in order to avoid student answering questions randomly and having nonsensical answers.

```
Q1 == 1 AND Q2 == 0 IS -2
```

Which means that if a student was right for the question 1, but was not for question 2, he will get a malus of -2 points.



It creates a `Logic` object. Give it the formula as a string and it will process the information.

For example :

```python
def main():
	command = input('Enter a logic command:\n')
	logic = Logic(command)

  # To be later implemented
  newResults = logic.checkResults(oldResults)
```



You can later give the `Logic` object the full results of a student and it will adjust the final grade.
