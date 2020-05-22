# Name: Binance Pump and Dump Detector
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Detects pump and dumps from Binance crypto data.

# from __future__ import annotations
from typing import Dict, List
import random
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import feature_column
from matplotlib import pyplot as plt
from tensorflow.keras import layers

from models.LayerParameter import LayerParameter
from models.Hyperparameters import Hyperparameters
from models.PumpAndDumpDetector import PumpAndDumpDetector


class CryptoPumpAndDumpDetector(PumpAndDumpDetector):
    hyperparameters: Hyperparameters
    listOfMetrics: List
    exportPath: str

    _metrics: List

    _NUMBER_OF_SAMPLES = 25

    def __init__(self):
        super().__init__()
        self._buildMetrics()
        self.exportPath = "./model_exports/cryptopumpanddumpdetector"

        # The following lines adjust the granularity of reporting.
        pd.options.display.max_rows = 10
        pd.options.display.float_format = "{:.1f}".format
        # tf.keras.backend.set_floatx('float32')

    def setup(self, classificationThreshold: float, hyperparameters: Hyperparameters):
        super().setClassificationThreshold(classificationThreshold)
        self.hyperparameters = hyperparameters

    """
    Precondition: prices is a pandas dataframe or series.
    """
    def detect(self, prices) -> bool:
        # if isinstance(prices, pd.DataFrame):
        #     data = {name: np.array(value) for name, value in prices.items()}
        if isinstance(prices, pd.Series):
            data = {name: np.array([value]) for name, value in prices.iteritems()}
        elif isinstance(prices, List) or isinstance(prices, np.ndarray):
            # The list better contain only floats...
            data = self._turnListOfFloatsToInputData(prices)
        else:
            print("CryptoPumpAndDumpDetector detect() had its precondition "
                  "violated!")
            return False

        if data is None or len(data) < CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES * 2:
            print("CryptoPumpAndDumpDetector detect() was not given enough "
                  "data to work with!")
            print(len(data))
            return False

        result = self.model.predict(data)[0][0]
        print("Gave out a result of " + str(result))
        return result <= self._classificationThreshold

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

    def trainModel(self, dataset: pd.DataFrame, label_name):
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

    def exportWeights(self):
        self.model.save_weights(self.exportPath)

    def loadWeights(self):
        self.model.load_weights(self.exportPath)

    def createModelUsingDefaults(self):
        featureColumns = []

        for i in range(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES):
            c = tf.feature_column.numeric_column("Volume-RA-" + str(i))
            featureColumns.append(c)

        for i in range(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES):
            c = tf.feature_column.numeric_column("Price-RA-" + str(i))
            featureColumns.append(c)

        # Convert the list of feature columns into a layer that will later be fed into
        # the model.
        featureLayer = layers.DenseFeatures(featureColumns)
        layerParameters = [
            LayerParameter(5, "sigmoid")
        ]

        self.createModel(featureLayer, layerParameters)

    def setupUsingDefaults(self):
        # Hyperparameters!
        learningRate = 0.008
        epochs = 500
        batchSize = 30
        classificationThreshold = 0.5
        self.setup(classificationThreshold,
                    Hyperparameters(learningRate, epochs,
                                    batchSize))

    def _turnListOfFloatsToInputData(self, data: List[float]) -> Dict:
        if len(data) < CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES * 2:
            print("DATA LEN: " + str(len(data)))
            return None

        features = {}
        j = 0

        for i in range(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES):
            features["Volume-RA-" + str(i)] = data[j]
            j += 1

        for i in range(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES):
            features["Price-RA-" + str(i)] = data[j]
            j += 1

        return features

    def _buildMetrics(self):
        self._metrics = [
            tf.keras.metrics.BinaryAccuracy(name='accuracy',
                                      threshold=self._classificationThreshold),
            tf.keras.metrics.Precision(thresholds=self._classificationThreshold,
                                     name='precision'
                                     ),
            tf.keras.metrics.Recall(thresholds=self._classificationThreshold,
                                  name="recall"),
            tf.keras.metrics.AUC(num_thresholds=100, name='auc'),
                             tf.keras.metrics.MeanSquaredError(name='rmse')
        ]
        self.listOfMetrics = ["accuracy", "precision", "recall", "auc", "rmse"]

