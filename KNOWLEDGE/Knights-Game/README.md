# What is this project?
- This is a simple propositional logic problem, it is based on the book made by logician Raymond Smullyan in 1978, titled “What is the name of this book?”
- The problem works as follows, the reader is expected to determine using logic which character included in a short statement is a knight and which character is a knave.
  - Knights always tell the truth
  - Knaves always lie
# What does it solve?
- In this project, there are two files
### logic.py
- it implements propositional logic operators
### puzzle.py
- it writes increasingly complex statements in propositional logic in order to create a knowledge base for the AI to determine the identity of the Knights and the Knaves

### EXAMPLE
```
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(
    Or(AKnave, AKnight),
    Or(BKnave, BKnight),
    Implication(AKnight, And(AKnave,BKnave)),
    Implication(AKnave, Or(And(AKnave,BKnight),And(BKnight,AKnight)))
)
```
# Credit and sources
- Credit to the design of the project and logic.py goes to Harvard university and the CS50 course
- https://cs50.harvard.edu/ai/2020/projects/1/knights/
