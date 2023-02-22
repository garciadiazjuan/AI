# What is this project?
- This is an search AI that, trained with a csv, can find a path connecting two nodes, in this case, it connects actors in hollywood by movies they have starred in 
# What does it solve?
- In this project, there are two main files
### degrees.py
File that:
- loads data
- finds shortest path between actors
### util.py
- implements a stack and a queue frontier, which can be selected in runtime to approach the search in a different manner
### AI
- The most interesting part of this AI model, is the following function which finds the shortest path using BFS
```
def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.
    If no possible path, returns None.
    """
    #i am doing BFS as it finds always the shortest path
    
    # TODO
    num_explored = 0
    
    #add source person id movies to frontier
    start = Node(state = source, parent = None, action = neighbors_for_person(source))
    frontier = QueueFrontier()
    frontier.add(start)
    
    explored = set()
    #while frontier is not empty
    while (True):
        if frontier.empty():
            raise Exception("no solution")
        #expand first in person
        node = frontier.remove()
        num_explored += 1
        
        if node.state == target:
            actions = []
            while node.parent is not None:
                actions.append(node.action)
                node = node.parent
            actions.reverse()
            return actions
        explored.add(node.state)
        
        for actions in neighbors_for_person(node.state):
            if not frontier.contains_state(actions[1]) and actions[1] not in explored:
                child = Node(state = actions[1], parent = node, action = actions)
                frontier.add(child)
```

### How the output looks
![alt text](https://github.com/garciadiazjuan/AI/blob/main/SEARCH%20PROBLEMS/Degrees/images/example_output.png)

# Credit and sources
- Credit to the design of the project and base code goes to Harvard university and the CS50 course
- [https://cs50.harvard.edu/ai/2020/projects/0/degrees/](https://cs50.harvard.edu/ai/2020/projects/0/degrees/)
