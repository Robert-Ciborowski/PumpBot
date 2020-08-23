# Name: Hyperparameters
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Stores hyperparameters to a machine learning model.

class Hyperparameters:
    learningRate: float
    epochs: int
    batchSize: int
    decayRate: float
    decayStep: float

    def __init__(self, learningRate: float, epochs: int, batchSize=None, decayRate=0.5, decayStep=1.0):
        self.learningRate = learningRate
        self.epochs = epochs
        self.batchSize = batchSize
        self.decayRate = decayRate
        self.decayStep = decayStep
