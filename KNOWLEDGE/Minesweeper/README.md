# What is this project?
- This is a simple propositional logic AI, that attempts to solve minesweeper using a knowledge base
# What does it solve?
- In this project, there are two files
### minesweeper.py
- it implements a simplified version of the minesweeper game
### runner.py
- sets up the game and decides the next move based on the knowledge base
### AI
```
 def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        
        #2) mark the cell as safe
        self.mark_safe(cell)


        #3) add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        neighbors = self.neighbors(cell)
        mineCounter = count
        newNeighbors = set()
        for neighbor in neighbors:
            if neighbor in self.mines:
                newNeighbors.add(neighbor)
                mineCounter -= 1
            if neighbor in self.safes:
                newNeighbors.add(neighbor)
        neighbors -= newNeighbors
        newSentence = Sentence(neighbors, mineCounter)
        self.knowledge.append(newSentence)

        #4) mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        newSafes = set()
        newMines = set()
        for sentence in self.knowledge:
            for mine in sentence.known_mines():
                newMines.add(mine)
            for safe in sentence.known_safes():
                newSafes.add(safe)
        for mine in newMines:
            self.mark_mine(mine)
        for safe in newSafes:
            self.mark_safe(safe)


        # delete empty sentences
        sentencesToRemove = []
        for sentence in self.knowledge:
            if sentence.cells == set():
                sentencesToRemove.append(sentence)
        for sentence in sentencesToRemove:
            self.knowledge.remove(sentence)

        #5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge
        sentencesToAdd = []
        for sentence in self.knowledge:
            if newSentence.cells and sentence.cells != newSentence.cells:
                if sentence.cells.issubset(newSentence.cells):
                    toAdd = Sentence(newSentence.cells-sentence.cells, newSentence.count-sentence.count)
                    sentencesToAdd.append(toAdd)
                if newSentence.cells.issubset(sentence.cells):
                    toAdd = Sentence(sentence.cells-newSentence.cells, sentence.count-newSentence.count)
                    sentencesToAdd.append(toAdd)
        self.knowledge += sentencesToAdd
```
### How the game looks
![alt text](https://github.com/garciadiazjuan/AI/blob/main/KNOWLEDGE/Minesweeper/images/minsweeper.png?raw=true)

# Credit and sources
- Credit to the design of the project and logic.py goes to Harvard university and the CS50 course
- https://cs50.harvard.edu/ai/2020/projects/1/minesweeper/
