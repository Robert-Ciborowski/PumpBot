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
from models.Hyperparameters import Hyperparameters
from models.PumpAndDumpDetector import PumpAndDumpDetector


class CryptoPumpAndDumpDetector(PumpAndDumpDetector):
    hyperparameters: Hyperparameters
    listOfMetrics: List
    _metrics: List

    def __init__(self, classificationThreshold: float, hyperparameters: Hyperparameters):
        super().__init__(classificationThreshold)
        self._buildMetrics()
        self.hyperparameters = hyperparameters

    def detect(self, prices: List[int]) -> bool:
        return random.random() <= self._classificationThreshold

    """
    Creates a brand new neural network for this model.
    """
    def createModel(self, featureLayer,
                     layerParameters: List):
        self.model = tf.keras.models.Sequential()
        self.model.add(featureLayer)

        count = 0
        for parameter in layerParameters:
            self.model.add(tf.keras.layers.Dense(units=parameter.units,
                                            activation=parameter.activation,
                                            kernel_regularizer=tf.keras.regularizers.l2(
                                                l=0.04),
                                            name="Hidden_" + str(count)))
            count += 1

        # Define the output layer.
        self.model.add(tf.keras.layers.Dense(units=1, input_shape=(1,),
                                activation=tf.sigmoid, name="Output"))

        # Compiles the model with the appropriate loss function.
        self.model.compile(
            optimizer=tf.keras.optimizers.RMSprop(lr=self.hyperparameters.learningRate),
            loss=tf.keras.losses.BinaryCrossentropy(), metrics=self._metrics)

    def trainModel(self, dataset, label_name):
        """Train the model by feeding it data."""

        # Split the dataset into features and label.
        features = {name: np.array(value) for name, value in dataset.items()}
        label = np.array(features.pop(label_name))
        history = self.model.fit(x=features, y=label, batch_size=self.hyperparameters.batchSize,
                            epochs=self.hyperparameters.epochs, shuffle=True)

        # The list of epochs is stored separately from the rest of history.
        epochs = history.epoch

        # To track the progression of training, gather a snapshot
        # of the model's mean squared error at each epoch.
        hist = pd.DataFrame(history.history)
        return epochs, hist

    """
    Evalutaes the model on features.
    Returns:
        Scalar test loss (if the model has a single output and no metrics)
        or list of scalars (if the model has multiple outputs
        and/or metrics). The attribute `model.metrics_names` will give you
        the display labels for the scalar outputs.
    """
    def evaluate(self, features, label):
        return self.model.evaluate(features, label, self.hyperparameters.batchSize)

    def plotCurve(self, epochs, hist, metrics):
        """Plot a curve of one or more classification metrics vs. epoch."""
        # list_of_metrics should be one of the names shown in:
        # https://www.tensorflow.org/tutorials/structured_data/imbalanced_data#define_the_model_and_metrics

        plt.figure()
        plt.xlabel("Epoch")
        plt.ylabel("Value")

        for m in metrics:
            x = hist[m]
            plt.plot(epochs[1:], x[1:], label=m)

        plt.legend()
        plt.show()

    def _buildMetrics(self):
        self._metrics = [tf.keras.metrics.BinaryAccuracy(name='accuracy',
                                      threshold=self._classificationThreshold),
      tf.keras.metrics.Precision(thresholds=self._classificationThreshold,
                                 name='precision'
                                 ),
      tf.keras.metrics.Recall(thresholds=self._classificationThreshold,
                              name="recall"),
        tf.keras.metrics.AUC(num_thresholds=100, name='auc'),
                         tf.keras.metrics.MeanSquaredError(name='rmse')]
        self.listOfMetrics = ["accuracy", "precision", "recall", "auc", "rmse"]
