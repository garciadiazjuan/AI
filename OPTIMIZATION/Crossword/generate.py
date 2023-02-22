import sys
import operator
from copy import deepcopy

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

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
            

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:
            if variable not in assignment:
                return False
        for variable in assignment:
            if len(assignment[variable]) == 0:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        values = set()
        for variable in assignment:
            # make sure all assigned values are unique
            if assignment[variable] not in values:
                values.add(assignment[variable])
            else:
                return False
            # make sure all assigned values have the correct length
            if variable.length != len(assignment[variable]):
                return False
            # no conflicts between neighbouring variables
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    overlap = self.crossword.overlaps[variable,neighbor]
                    varIndex = overlap[0]
                    neighborIndex = overlap[1]
                    word = assignment[variable]
                    neighborWord = assignment[neighbor]
                    if word[varIndex] != neighborWord[neighborIndex]:
                        return False
        return True
                
    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # calculate count of words that would be ruled out for each possible word i can assign to var
        for value in self.domains[var]:
            domain_values = dict()
            count = 0
            for neighbor in self.crossword.neighbors(var):
                if neighbor not in assigment:
                    overlap = self.domains.overlaps[variable,neighbor]
                    varIndex = overlap[0]
                    neighborIndex = overlap[1]
                    for word in self.domains[neighbor]:
                        if value[varIndex] != word[neighborIndex]:
                            count += 1
                    domain_values[value] = count
        # add them in a sorted list with descending order
        sorted_domain_values = sorted(domain_values.items(), key=operator.itemgetter(1))
        return sorted_domain_values.keys()
                    
                

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        first_one = True
        min_variable = None
        min_values = None
        max_degree = None
        # for all variables
        for var in self.domains:
            # if var not in assignment
            if var not in assignment:
                # assign first value
                if first_one:
                    min_variable = var
                    min_values = len(self.domains[var])
                    max_degree = len(self.crossword.neighbors(var))
                    first_one = False
                # check if current var has less values than saved one
                elif min_values > len(self.domains[var]):
                    min_variable = var
                    min_values = len(self.domains[var])
                    max_degree = len(self.crossword.neighbors(var))
                # check if current var has equal nr of values than saved one and has higher degree   
                elif min_values == len(self.domains[var]) and max_degree < len(self.crossword.neighbors(var)):
                    min_variable = var
                    min_values = len(self.domains[var])
                    max_degree = len(self.crossword.neighbors(var))
        return min_variable
        

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.domains[var]:
            newAssignment = assignment.copy()
            newAssignment[var] = value
            if self.consistent(newAssignment):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result != None:
                    return result
                del assignment[var]
        return None

def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
