# Name: Layer Parameter
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: A parameter for a neural network layer.

class LayerParamater:
    # Number of nodes in the layer
    units: int
    # Activation function for the layer, e.g. "relu" or "sigmoid"
    activation: str

    def __init__(self, units: int, activation="relu"):
        self.units = units
        self.activation = activation
