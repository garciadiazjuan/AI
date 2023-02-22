import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from copy import deepcopy

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # for each row in the csv
    # store all row values except label on a list
    # store that list in the list of all data
    # add label value to labels list
    evidence_list = list()
    labels_list = list()
    with open(filename) as f:
        f.readline() # Skip header line
        csvin = csv.reader(f)
        for row in csvin:
            #format values in accordance to specification
            months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
            count = 0
            actualCount = 0
            for month in months:
                if row[10] == month:
                    actualCount = count
                count += 1
            visitor_type = None
            if row[15] == "Returning_Visitor":
                visitor_type = 1
            else: 
                visitor_type = 0
            weekend = row[16]
            if weekend == "TRUE":
                weekend = 1
            else:
                weekend = 0
            evidence_values = [int(row[0]), float(row[1]), int(row[2]), float(row[3]), int(row[4]), 
            float(row[5]) , float(row[6]), float(row[7]), float(row[8]), float(row[9]), actualCount,
            int(row[11]),int(row[12]),int(row[13]),int(row[14]), visitor_type, weekend]
            
            label_values = row[17]
            label = 0
            if label_values == "TRUE":
                label = 1
            evidence_list.append(evidence_values)
            labels_list.append(label)
    return (evidence_list,labels_list)

def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    model = KNeighborsClassifier(n_neighbors=1)
    return model.fit(evidence,labels)
    

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    positives = 0
    positive_count = 0
    negative_count = 0
    for (labelVal, predictionVal) in zip(labels, predictions):
        if labelVal == 1 and labelVal == predictionVal:
            positives += 1
            positive_count += 1
        elif labelVal == 1:
            positives += 1
        else:
            if labelVal == predictionVal:
                negative_count += 1
    sensitivity = positive_count/positives
    specificity = negative_count/(len(labels)-positives)
    return (sensitivity, specificity)


if __name__ == "__main__":
    main()
