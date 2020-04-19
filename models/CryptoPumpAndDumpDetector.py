# Name: Binance Pump and Dump Detector
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Detects pump and dumps from Binance crypto data.

# from __future__ import annotations
from typing import List
import random
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from matplotlib import pyplot as plt
import tensorflow.keras.layers

from models import LayerParameter
from models.PumpAndDumpDetector import PumpAndDumpDetector

class CryptoPumpAndDumpDetector(PumpAndDumpDetector):
    def __init__(self):
        super().__init__()

    def detect(self, prices: List[int]) -> bool:
        return random.random() <= self._classificationThreshold

    """
    Creates a brand new neural network for this model.
    """
    def createModel(self, learningRate: float, featureLayer,
                     layerParameters: List[LayerParameter], metrics=[]):
        # Most simple tf.keras models are sequential.
        model = tf.keras.models.Sequential()

        # Add the layer containing the feature columns to the model.
        model.add(featureLayer)

        count = 0
        for parameter in layerParameters:
            model.add(tf.keras.layers.Dense(units=parameter.units,
                                            activation=parameter.activation,
                                            kernel_regularizer=tf.keras.regularizers.l2(
                                                l=0.04),
                                            name="Hidden_" + str(count)))
            count += 1

        # Define the output layer.
        model.add(tf.keras.layers.Dense(units=1,
                                        name="Output"))

        # Use mean squared error for the loss function.
        model.compile(
            optimizer=tf.keras.optimizers.RMSprop(lr=learningRate),
            loss=tf.keras.losses.BinaryCrossentropy(),
            metrics=metrics)

        return model

    def trainModel(model, dataset, epochs, label_name,
                           batch_size=None):
        """Train the model by feeding it data."""

        # Split the dataset into features and label.
        features = {name: np.array(value) for name, value in dataset.items()}
        label = np.array(features.pop(label_name))
        history = model.fit(x=features, y=label, batch_size=batch_size,
                            epochs=epochs, shuffle=True)

        # The list of epochs is stored separately from the rest of history.
        epochs = history.epoch

        # To track the progression of training, gather a snapshot
        # of the model's mean squared error at each epoch.
        hist = pd.DataFrame(history.history)
        mse = hist["mean_squared_error"]

        return epochs, mse
