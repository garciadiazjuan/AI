from cmath import log
import nltk
import sys
import os
from nltk.tokenize import word_tokenize
import operator
import math


FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    map = dict()
    for file in os.listdir(directory):
        with open(os.path.join(directory, file), "r") as f:
            data = f.read()
        map[file] = data
    return map
            


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    #tokenize all elements of document into list of individual words and symbols
    document = word_tokenize(document)
    # iterate through tokenized list
    processedWords = list()
    for word in document:
        # ensure individual words are all lowercase and contain at least one letter
        if word.isalpha() and not word in nltk.corpus.stopwords.words("english"): 
            processedWords.append(word.lower())
    return processedWords


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



def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    # get document tf-idf vals
    docVals = dict()
    for document in files:
        docIdf = 0
        for word in query:
            if word in files[document]:
                docIdf += (idfs[word] * files[document].count(word))
        if document in docVals:
            docVals[document] = docVals[document] + docIdf
        else:
            docVals[document] = docIdf
    # sort dict based on val and return top n
    sortedDocVals = dict(sorted(docVals.items(), key=operator.itemgetter(1), reverse=True))
    return [*sortedDocVals][:n]

        


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    # get sentence idf vals
    sentenceVals = dict()
    for document in sentences:
        docIdf = 0
        for word in query:
            if word in sentences[document]:
                docIdf += idfs[word] 
        sentenceVals[document] = docIdf
    # sort dict based on val and return top n
    sortedSentenceVals = dict(sorted(sentenceVals.items(), key=operator.itemgetter(1), reverse=True))
    return [*sortedSentenceVals][:n]
    

if __name__ == "__main__":
    main()
