# Name: Hyperparameters
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Stores hyperparameters to a machine learning model.

class Hyperparameters:
    learningRate: float
    epochs: int
    batchSize: int

    def __init__(self, learningRate: float, epochs: int, batchSize=None):
        self.learningRate = learningRate
        self.epochs = epochs
        self.batchSize = batchSize
