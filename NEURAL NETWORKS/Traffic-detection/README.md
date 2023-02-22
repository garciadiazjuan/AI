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
