# What is this project?
- This is a simple Machine learning model that plays nim and improves every game
# What does it solve?
- In this project, there are two main files
### nim.py
this file includes:
 - the rules of nim contained in a class with the same name
 - a simple ML implementing a Q learning model to expand on its knowledge base of q values
 - A "train" function, which trains the ML model
   
### play.py
- 3 lines of code that call the function to train the ML model
### AI
- The main function that powers this ML model is the following, which decides the best move based on q value estimates
```
 def choose_action(self, state, epsilon=True):
        """
        Given a state `state`, return an action `(i, j)` to take.
        If `epsilon` is `False`, then return the best action
        available in the state (the one with the highest Q-value,
        using 0 for pairs that have no Q-values).
        If `epsilon` is `True`, then with probability
        `self.epsilon` choose a random available action,
        otherwise choose the best action available.
        If multiple actions have the same Q-value, any of those
        options is an acceptable return value.
        """
        
        best_action = None
        best_q = None
        for action in Nim.available_actions(state):
            if best_action == None:
                best_action = action
                state = tuple(state)
                key = (state,action)
                if key not in self.q:
                    best_q = 0
                else:
                    best_q = self.q[key]
            else:
                state = tuple(state)
                key = (state,action)
                if key in self.q and best_q < self.q[key]:
                    best_q = self.q[key]
                    best_action = action
        
        if epsilon == False:
            # return best action
            return best_action
        else:
            choice = random.randint(0, 100)
            if choice > (100 -epsilon*100):
                for action in Nim.available_actions(state):
                    return action
            else: 
                return best_action
```
### How the output looks
![alt text](https://github.com/garciadiazjuan/AI/blob/main/LEARNING/Nim-game/images/nim_example.png)

# Credit and sources
- Credit to the design of the project and base code goes to Harvard university and the CS50 course
- [https://cs50.harvard.edu/ai/2020/projects/4/nim/](https://cs50.harvard.edu/ai/2020/projects/4/nim/)
