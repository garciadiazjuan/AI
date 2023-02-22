import nltk
import sys
from nltk.tokenize import word_tokenize
from sqlalchemy import false, true

TERMINALS = """
Adj -> "country" | "dreadful" | "enigmatical" | "little" | "moist" | "red"
Adv -> "down" | "here" | "never"
Conj -> "and" | "until"
Det -> "a" | "an" | "his" | "my" | "the"
N -> "armchair" | "companion" | "day" | "door" | "hand" | "he" | "himself"
N -> "holmes" | "home" | "i" | "mess" | "paint" | "palm" | "pipe" | "she"
N -> "smile" | "thursday" | "walk" | "we" | "word"
P -> "at" | "before" | "in" | "of" | "on" | "to"
V -> "arrived" | "came" | "chuckled" | "had" | "lit" | "said" | "sat"
V -> "smiled" | "tell" | "were"
"""

NONTERMINALS = """
S -> NP VP | S Conj S 
NP -> N | Det NP | P NP | NP NP | Adj NP 
VP -> VP NP | V | Adv VP | VP Adv | VP Conj VP
"""

Sentence = 'S'
NounPhrase = 'NP'
VerbPhrase = 'VP'

grammar = nltk.CFG.fromstring(NONTERMINALS + TERMINALS)
parser = nltk.ChartParser(grammar)


def main():

    # If filename specified, read sentence from file
    if len(sys.argv) == 2:
        with open(sys.argv[1]) as f:
            s = f.read()

    # Otherwise, get sentence as input
    else:
        s = input("Sentence: ")

    # Convert input into list of words
    s = preprocess(s)

    # Attempt to parse sentence
    try:
        trees = list(parser.parse(s))
    except ValueError as e:
        print(e)
        return
    if not trees:
        print("Could not parse sentence.")
        return

    # Print each tree with noun phrase chunks
    for tree in trees:
        tree.pretty_print()

        print("Noun Phrase Chunks")
        for np in np_chunk(tree):
            print(" ".join(np.flatten()))


def preprocess(sentence):
    """
    Convert `sentence` to a list of its words.
    Pre-process sentence by converting all characters to lowercase
    and removing any word that does not contain at least one alphabetic
    character.
    """
    #tokenize all elements of sentence into list of individual words and symbols
    sentence = word_tokenize(sentence)
    # iterate through tokenized list
    processedWords = list()
    for word in sentence:
        # ensure individual words are all lowercase and contain at least one letter
        if word.isalpha(): 
            processedWords.append(word.lower())
    return processedWords


def checkSubTrees(tree):
    """
    helper function used in np_chunk
    """
    # if the label of this subtree is NP i return true
    if tree.label() == NounPhrase:
        return True
    # if tree only has one child and its not a sentence(which can still contain a NP) return false
    if len(tree) == 1 and tree.label() != Sentence:
        return False 
    # if none of the previous are the case i recursively iterate over the children
    # of the subtree to check them instead
    for subtree in tree:
        if checkSubTrees(subtree):
            return True
    return False


def np_chunk(tree):
    """
    Return a list of all noun phrase chunks in the sentence tree.
    A noun phrase chunk is defined as any subtree of the sentence
    whose label is "NP" that does not itself contain any other
    noun phrases as subtrees.
    """
    chunks = list()
    # for each tree
    for subtree in tree:
        # get label and check if there is a NP on the subtrees
        node = subtree.label()
        hasNP = checkSubTrees(subtree)
        # if there isnt a NP we continue in the for loop
        if not hasNP:
            continue
        # if the label indicates that it is a noun phrase or the tree could contain
        # a noun phrase we check for subtrees and append if there is a NP that doesnt
        # contain a NP itself
        if node == NounPhrase or node == VerbPhrase or node == Sentence:
            subtreechild = np_chunk(subtree)
            for npChunk in subtreechild:
                chunks.append(npChunk)
    # if the label is NP and there are no subtrees inside append the NP chunk
    if tree.label() == NounPhrase and not hasNP:
        chunks.append(tree)
    return chunks
    


if __name__ == "__main__":
    main()
