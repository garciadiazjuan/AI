# What is this project?
- This is a simple Natural Language Processing project which answers simple queries from a small knowledge base
# What does it solve?
- In this project, there are two main files
### questions.py
Simple AI that:
- Loads files
- Tokenizes all words in the document
- Computes Inverse Dense Frequency
- Uses IDFS to find related files
- Finds relevant sentences to answer the query
### Corpus
- folder containing text files to feed the AI
### AI
- The most important function of the AI is the following, which computes values that allow the AI to find relevant IDF values
```
def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.
    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfVals = dict()
    for document in documents:
        for word in documents[document]:
            if not word in idfVals:
                docsItAppearsIn = 0
                for doc in documents:
                    if word in documents[doc]:
                        docsItAppearsIn += 1
                # avoid deviding by 0 
                if docsItAppearsIn == 0:
                    idfVals[word] = 0
                else:
                    idfVals[word] = math.log(len(documents)/ docsItAppearsIn)
            
    return idfVals
```
### How the output looks
![alt text](https://github.com/garciadiazjuan/AI/blob/main/LANGUAGE/Questions/images/example%20output.png)

# Credit and sources
- Credit to the design of the project and base code goes to Harvard university and the CS50 course
- [https://cs50.harvard.edu/ai/2020/projects/6/questions/](https://cs50.harvard.edu/ai/2020/projects/6/questions/)
