# What is this project?
- This is a tensorflow-based image proccessing application that uses neural networks to detect traffic
# What does it solve?
- In this project, there are two main files
### traffic.py
Simple ML that:
 - loads the csv data
 - Trains ML model
 - Evaluates ML model performance
### model.h5
- Tensorflow trained model 
### AI
- The most interesting part of this ML model, is the neural network i selected to tackle this problem:
```
def get_model():
    """
    Returns a compiled convolutional neural network model. Assume that the
    `input_shape` of the first layer is `(IMG_WIDTH, IMG_HEIGHT, 3)`.
    The output layer should have `NUM_CATEGORIES` units, one for each category.
    """
    model = Sequential(
        [

            #convolutional layer + pooling (can be done many times in this order)
            Conv2D(200, (8, 8), activation="relu", input_shape=(IMG_WIDTH, IMG_HEIGHT, 3)),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(250, (4, 4), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),
            Conv2D(250, (2, 2), activation="relu"),
            MaxPooling2D(pool_size=(2, 2)),

            # turn multidimensional input into one dimensional
            Flatten(),

            # add dense layer with relu activation
            Dense(450, activation="relu"),

            # dropout of 0.5 to not rely too much on certain nodes
            Dropout(0.5),

            # add dense layer with softmax activation
            Dense(NUM_CATEGORIES, activation="softmax"),

        ]
    )
    # summary
    model.summary()
    # compile
    model.compile(optimizer= "adam", loss = "categorical_crossentropy", metrics=["accuracy"])
    # return
    return model
```
# My experimentation process with TensorFlow and GTSRB
## After reading the documentation and taking a look at working examples, I started with the most basic version of a sequential model, using:
- One 2DConv()
- One Pooling with 2x2 dimensions
- One dense layer with (NUM_CATEGORIES and a softmax activation function)
**Observations** : runtime was fast, but accuracy was not good enough, due to the complexity of roadsigns not being linearly separable I decided to add a hidden layer

## Second attempt:
### after reading documentation on how to do hidden layers I added:
- 1 hidden layer with 350 nodes and rely activation
- Dropout of 0.5
**Observations** : runtime was slightly slower, but accuracy was not above my expected range of  > 95%

## Third attempt: 
### after playing with values I added:
- Two more conv2D + pooling functions
**Observations** : runtime was slower, but accuracy was above my expected range of  > 95% varying slightly with runtimes and averaging 97%

## Possible improvements
- One more hidden layer / adding more nodes to the existing hidden layer
- Use of a different, more complex model
- Increase dropout
- Change convoluting parameters
**Observations** : overall the accuracy is good enough and it would be interesting to give it a try with a faster computer

### How the output looks
![alt text](https://github.com/garciadiazjuan/AI/blob/main/NEURAL%20NETWORKS/Traffic-detection/images/example_output.png)

# Credit and sources
- Credit to the design of the project and base code goes to Harvard university and the CS50 course
- [https://cs50.harvard.edu/ai/2020/projects/5/traffic/](https://cs50.harvard.edu/ai/2020/projects/5/traffic/)

