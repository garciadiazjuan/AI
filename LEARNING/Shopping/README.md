# What is this project?
- This is a simple Machine Learning model that aims to predict if a customer made an online purchase based on collected data
# What does it solve?
- In this project, there are two main files
### shopping.py
Simple ML that:
 - loads the csv data
 - Trains ML model
 - Evaluates ML model performance
### Shopping.csv
- file of comma separated values containing data points and truth labels to feed and test the ML model.
### AI
- The most interesting part of this ML model, is the function that loads data and records each value and label:
```
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
```
### How the output looks
![alt text](https://github.com/garciadiazjuan/AI/blob/main/LEARNING/Shopping/images/output_shopping.png)

# Credit and sources
- Credit to the design of the project and base code goes to Harvard university and the CS50 course
- [https://cs50.harvard.edu/ai/2020/projects/4/shopping/](https://cs50.harvard.edu/ai/2020/projects/4/shopping/)
