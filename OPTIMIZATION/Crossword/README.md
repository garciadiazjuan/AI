# What is this project?
- This is an optimization AI capable of solving crosswords
# What does it solve?
- In this project, there are two main files
### crossword.py
File containing:
- Variable class, which acts as a word placeholder
- Crossword class which is made up of instances of the "variable" class
### generate.py
- Class that initializes the game and implements the AI and knowledge base by enforcing node consistency
### AI
- The most interesting part of this AI model, are the following 3 values that enforce node consistency
```
 def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        domaincopy = deepcopy(self.domains)
        for variable in self.domains:
            for word in domaincopy[variable]:
                if len(word) != variable.length:
                    self.domains[variable].remove(word)
        

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.
        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        # find shared letter index for both words
        overlap = self.crossword.overlaps[x,y]
        if overlap is None or x == y:
            return False
        # ensure that the words in domain x have a word in domain y that matches the letters
        # in the shared cell
        domaincopy = deepcopy(self.domains)
        revisionMade = False
        for wordX in domaincopy[x]:
            found = False
            for wordY in self.domains[y]:
                if wordX[overlap[0]] == wordY[overlap[1]]:
                    found = True
            if found == False:
                self.domains[x].remove(wordX)
                revisionMade = True
                
        return revisionMade
            

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.
        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        #make queue to store the arcs 
        if arcs == None:
            arcs = list()
            for variable in self.domains: 
                neighbours = self.crossword.neighbors(variable)
                for neighbour in neighbours:
                    if neighbour != variable:
                        arcs.append((variable,neighbour))
                
            
        while len(arcs) > 0:
            #revise x and y
            arcToCheck = arcs.pop(0)
            revisionMade = self.revise(arcToCheck[0],arcToCheck[1])
            # if revision is made we add all x neighbours against x again
            if revisionMade:
                neighbours = self.crossword.neighbors(arcToCheck[0])
                for neighbour in neighbours:
                    arcs.append((neighbour,arcToCheck[0]))
                # check if x domain is now empty
                # if it is return false
                if len(self.domains[arcToCheck[0]]) == 0:
                    return False
        # return true if all variables have a non empty domain
        return True
```

### How the game looks
![alt text](https://github.com/garciadiazjuan/AI/blob/main/OPTIMIZATION/Crossword/images/example_output.png)

# Credit and sources
- Credit to the design of the project and base code goes to Harvard university and the CS50 course
- [https://cs50.harvard.edu/ai/2020/projects/3/crossword/](https://cs50.harvard.edu/ai/2020/projects/3/crossword/)

