# What is this project?
- This is an search AI that, uses a minimax function to always make the best move in tictactoe
# What does it solve?
- In this project, there are two main files
### tictactoe.py
File that implements:
- board logic
- minimax search AI
### runner.py
- pygame file in charge of the visuals
### AI
- The most interesting part of this AI model, is the following function which calculates the best action using minimax
```
def minimaxCalculate(auxiliaryBoard, depth, isMaximizingPlayer):
   if terminal(auxiliaryBoard):
       return utility(auxiliaryBoard)
   elif isMaximizingPlayer and not terminal(auxiliaryBoard):
       bestVal = -math.inf
       for action in actions(auxiliaryBoard):
           currentBoard = auxiliaryBoard
           value = minimaxCalculate(result(currentBoard,action), depth+1, False)
           bestVal = max(bestVal, value)
       return bestVal
   else:
       bestVal = math.inf
       for action in actions(auxiliaryBoard):
           currentBoard = auxiliaryBoard
           value = minimaxCalculate(result(currentBoard,action), depth+1, True)
           bestVal = min(bestVal, value)
       return bestVal
```

### How the game looks
![alt text](https://github.com/garciadiazjuan/AI/blob/main/SEARCH%20PROBLEMS/Tictactoe/images/tictactoe.png)

# Credit and sources
- Credit to the design of the project and base code goes to Harvard university and the CS50 course
- [https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/](https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/)
