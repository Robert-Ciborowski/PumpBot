# Name: Binance Pump and Dump Detector
# Author: Robert Ciborowski
# Date: 18/04/2020
# Description: Detects pump and dumps from Binance crypto data.

# from __future__ import annotations
import os
from datetime import datetime
from typing import Dict, List
import random
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_model_optimization as tfmot
from tensorflow import feature_column
from matplotlib import pyplot as plt
from tensorflow.keras import layers
from tensorflow.python.keras import Input

from models.LayerParameter import LayerParameter
from models.Hyperparameters import Hyperparameters
from models.PumpAndDumpDetector import PumpAndDumpDetector
from thread_runner.ThreadRunner import ThreadRunner
from util.Constants import GROUPED_DATA_SIZE, SAMPLES_OF_DATA_TO_LOOK_AT
import threading as th


class CryptoPumpAndDumpDetector(PumpAndDumpDetector):
    hyperparameters: Hyperparameters
    listOfMetrics: List
    exportPath: str

    _metrics: List
    _NUMBER_OF_SAMPLES = SAMPLES_OF_DATA_TO_LOOK_AT
    # _DATA_LENGTH_FOR_MODEL = int(_NUMBER_OF_SAMPLES * 2 / GROUPED_DATA_SIZE)\
    #                          + int(_NUMBER_OF_SAMPLES / GROUPED_DATA_SIZE)\
    #                          + int(_NUMBER_OF_SAMPLES * 2 / (GROUPED_DATA_SIZE * 3))
    _DATA_LENGTH_FOR_MODEL = _NUMBER_OF_SAMPLES

    def __init__(self, tryUsingGPU=False):
        super().__init__()

        if not tryUsingGPU:
            os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        else:
            self._configureForGPU()

        self.exportPath = "./model_exports/cryptopumpanddumpdetector"

        # The following lines adjust the granularity of reporting.
        pd.options.display.max_rows = 10
        pd.options.display.float_format = "{:.1f}".format
        # tf.keras.backend.set_floatx('float32')

    def setup(self, classificationThreshold: float, hyperparameters: Hyperparameters):
        super().setClassificationThreshold(classificationThreshold)
        self._buildMetrics()
        self.hyperparameters = hyperparameters

    """
    Precondition: prices is a pandas dataframe or series.
    """
    def detect(self, prices, volumes) -> float:
        # if isinstance(prices, pd.DataFrame):
        #     data = {name: np.array(np.float32(value)) for name, value in
        #             volumes.items()}
        #     data += {name: np.array(np.float32(value)) for name, value in
        #             prices.items()}
        # if isinstance(prices, pd.Series):
        #     data = {name: np.array([np.float32(value)]) for name, value in
        #             volumes.iteritems()}
        #     data += {name: np.array([np.float32(value)]) for name, value in
        #             prices.iteritems()}
        if isinstance(prices, List) or isinstance(prices, np.ndarray):
            # volumes2 = pd.Series(volumes)
            # volumesStd = volumes2.std()
            # prices2 = pd.Series(prices)
            # pricesStd = prices2.std()

            # if pricesStd >= 2.0e-8:
            #     return 0

            # The input data better contain only floats...
            data = self._setupDataForModelUsingZScores2(prices, volumes)
            # prices, volumes = self._setupDataForModelUsingZScores(prices, volumes)
            # prices, volumes, prices2, volumes2, prices3, volumes3 = self._setupDataForModelUsingFractions(prices, volumes)
            # data = self._turnListOfFloatsToInputData(volumes + prices + prices2 + volumes2 + prices3 + volumes3, len(volumes), len(prices))
            # data = volumes + prices
        # elif isinstance(prices, Dict):
        #     data = volumes + prices
        else:
            print("CryptoPumpAndDumpDetector detect() had its precondition "
                  "violated!")
            return 0.0

        if data is None or len(data) != CryptoPumpAndDumpDetector._DATA_LENGTH_FOR_MODEL:
            print("CryptoPumpAndDumpDetector detect() was not given enough "
                  "data to work with! Data is None: " + str(data is None))
            if data is not None:
                print("(length of data: " + str(len(data)) + ", expected: "
                      + str(CryptoPumpAndDumpDetector._DATA_LENGTH_FOR_MODEL) + ")")
            return 0.0

        return self._detect(data)

    def _detect(self, data) -> float:
        time1 = datetime.now()
        data = np.array([data])
        result = self.model.predict(data)[0][0]
        # result = self.model(data).numpy()[0][0]
        time2 = datetime.now()
        print("Gave out a result of " + str(result) + ", took " + str(
            time2 - time1))
        return result

    def _setupDataForModelUsingFractions(self, inputPrices, inputVolumes):
        volumeMax = np.amax(inputVolumes)
        pricesMax = np.amax(inputPrices)

        if volumeMax == 0.0:
            volumeMax = 1.0

        if pricesMax == 0.0:
            pricesMax = 1.0

        volumes = []
        prices = []
        volumes2 = []
        prices2 = []
        volumes3 = []
        prices3 = []
        collectiveVolume = 0.0
        collectivePrice = 0.0
        subsectionSize = GROUPED_DATA_SIZE

        index = 0

        for item in inputPrices:
            collectivePrice += item
            index += 1

            if index == subsectionSize:
                index = 0
                prices.append(np.array([collectivePrice / subsectionSize / pricesMax]))
                collectivePrice = 0.0

        index = 0

        for item in inputVolumes:
            collectiveVolume += item
            index += 1

            if index == subsectionSize:
                index = 0
                volumes.append(np.array([collectiveVolume / subsectionSize / volumeMax]))
                collectiveVolume = 0.0

        subsectionSize = GROUPED_DATA_SIZE * 2

        index = 0

        for item in inputPrices:
            collectivePrice += item
            index += 1

            if index == subsectionSize:
                index = 0
                prices2.append(
                    np.array([collectivePrice / subsectionSize / pricesMax]))
                collectivePrice = 0.0

        index = 0

        for item in inputVolumes:
            collectiveVolume += item
            index += 1

            if index == subsectionSize:
                index = 0
                volumes2.append(
                    np.array([collectiveVolume / subsectionSize / volumeMax]))
                collectiveVolume = 0.0

        index = 0
        subsectionSize = GROUPED_DATA_SIZE * 3

        for item in inputPrices:
            collectivePrice += item
            index += 1

            if index == subsectionSize:
                index = 0
                prices3.append(
                    np.array([collectivePrice / subsectionSize / pricesMax]))
                collectivePrice = 0.0

        index = 0

        for item in inputVolumes:
            collectiveVolume += item
            index += 1

            if index == subsectionSize:
                index = 0
                volumes3.append(
                    np.array([collectiveVolume / subsectionSize / volumeMax]))
                collectiveVolume = 0.0

        return prices, volumes, prices2, volumes2, prices3, volumes3

    def _setupDataForModelUsingZScores(self, prices, volumes):
        from scipy import stats
        prices = stats.zscore(prices)
        volumes = stats.zscore(volumes)
        prices = [np.array([x]) for x in prices]
        volumes = [np.array([x]) for x in volumes]
        return prices, volumes

    def _setupDataForModelUsingZScores2(self, prices, volumes):
        from scipy import stats
        prices = stats.zscore(prices)
        volumes = stats.zscore(volumes)
        prices = [np.array(abs(x)) for x in prices]
        volumes = [np.array(abs(x)) for x in volumes]
        priceMax = np.amax(prices)
        volumeMax = np.amax(volumes)

        if volumeMax < 750:
            volumeMax = 750

        if priceMax == 0.0:
            priceMax = 1.0

        prices = [x / priceMax for x in prices]
        volumes = [x / volumeMax for x in volumes]
        data = []

        for i in range(len(prices)):
            data.append((prices[i], volumes[i]))

        return np.array(data)

    """
    Creates a brand new neural network for this model.
    """
    def createModel(self, featureLayer,
                     layerParameters: List):
        # Should go over minutes, not seconds
        # input_seq = layers.Input(shape=(SAMPLES_OF_DATA_TO_LOOK_AT, 1))
        self.model = tf.keras.models.Sequential()
        self.model.add(layers.Conv1D(filters=16, kernel_size=6, activation='relu',
                         input_shape=(SAMPLES_OF_DATA_TO_LOOK_AT, 2)))
        self.model.add(layers.MaxPooling1D(pool_size=2))
        self.model.add(
            layers.Conv1D(filters=8, kernel_size=4, activation='relu',
                          input_shape=(SAMPLES_OF_DATA_TO_LOOK_AT, 2)))
        self.model.add(layers.MaxPooling1D(pool_size=2))
        self.model.add(
            layers.Conv1D(filters=4, kernel_size=2, activation='relu',
                          input_shape=(SAMPLES_OF_DATA_TO_LOOK_AT, 2)))
        self.model.add(layers.MaxPooling1D(pool_size=4))
        self.model.add(layers.Flatten())
        self.model.add(layers.Dense(20, activation='relu'))
        self.model.add(layers.Dense(10, activation='relu'))
        self.model.add(tf.keras.layers.Dropout(0.4))
        self.model.add(layers.Dense(1, activation='sigmoid'))
        self.model.compile(loss='binary_crossentropy',
            optimizer=tf.keras.optimizers.RMSprop(lr=self.hyperparameters.learningRate),
            metrics=self._metrics)


        # self.model = tf.keras.models.Sequential()
        # self.model.add(featureLayer)
        #
        # self.model.add(layers.Conv1D(16, 6, activation='relu'))
        # self.model.add(layers.MaxPooling1D(4))
        #
        # # self.model.add(layers.Conv1D(32, 6, activation='relu'))
        # # self.model.add(layers.MaxPooling1D(4))
        # #
        # # self.model.add(layers.Conv1D(64, 6, activation='relu'))
        # # self.model.add(layers.MaxPooling1D(4))
        #
        # self.model.add(layers.Dense(512, activation='relu'))
        #
        # self.model.add(layers.Dense(1, activation='sigmoid'))
        #
        # self.model.compile(loss='binary_crossentropy',
        #     optimizer=tf.keras.optimizers.RMSprop(lr=self.hyperparameters.learningRate),
        #     metrics=self._metrics)

        # self.model = tf.keras.models.Sequential()
        # self.model.add(featureLayer)
        #
        # count = 0
        # for parameter in layerParameters:
        #     self.model.add(tf.keras.layers.Dense(units=parameter.units,
        #                                     activation=parameter.activation,
        #                                     # kernel_regularizer=tf.keras.regularizers.l2(
        #                                     #     l=0.04),
        #                                     name="Hidden_" + str(count)))
        #     count += 1
        #
        # # self.model.add(tf.keras.layers.Dropout(0.05))
        #
        # # Define the output layer.
        # self.model.add(tf.keras.layers.Dense(units=1, input_shape=(1,),
        #                         activation=tf.sigmoid, name="Output"))
        #
        # scheduler = tf.keras.optimizers.schedules.InverseTimeDecay(
        #     self.hyperparameters.learningRate, self.hyperparameters.decayStep,
        #     self.hyperparameters.decayRate, staircase=False)
        #
        # # Compiles the model with the appropriate loss function.
        # self.model.compile(
        #     optimizer=tf.keras.optimizers.Adam(scheduler),
        #     # optimizer=tf.keras.optimizers.RMSprop(scheduler),
        #     loss=tf.keras.losses.BinaryCrossentropy(), metrics=self._metrics)

    # def trainModel(self, dataset: pd.DataFrame, validationSplit: float, label_name):
    def trainModel(self, features, labels, validationSplit: float):
        """Train the model by feeding it data."""
        # Split the dataset into features and label.
        # features = {name: np.array(value) for name, value in dataset.items()}
        # label = np.array(features.pop(label_name))
        # history = self.model.fit(x=features, y=label,
        #                          batch_size=self.hyperparameters.batchSize,
        #                          validation_split=validationSplit,
        #                          epochs=self.hyperparameters.epochs,
        #                          shuffle=True)
        history = self.model.fit(x=features, y=labels, batch_size=self.hyperparameters.batchSize,
                            validation_split=validationSplit, epochs=self.hyperparameters.epochs, shuffle=True)

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

        # for i in range(int(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES / GROUPED_DATA_SIZE)):
        #     c = tf.feature_column.numeric_column("Volume-RA-" + str(i))
        #     featureColumns.append(c)
        #
        # for i in range(int(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES / GROUPED_DATA_SIZE)):
        #     c = tf.feature_column.numeric_column("Price-RA-" + str(i))
        #     featureColumns.append(c)

        # for i in range(int(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES / GROUPED_DATA_SIZE / 2)):
        #     c = tf.feature_column.numeric_column("Volume-RA2-" + str(i))
        #     featureColumns.append(c)
        #
        # for i in range(int(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES / GROUPED_DATA_SIZE / 2)):
        #     c = tf.feature_column.numeric_column("Price-RA2-" + str(i))
        #     featureColumns.append(c)
        #
        # for i in range(int(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES / GROUPED_DATA_SIZE / 3)):
        #     c = tf.feature_column.numeric_column("Volume-RA3-" + str(i))
        #     featureColumns.append(c)
        #
        # for i in range(int(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES / GROUPED_DATA_SIZE / 3)):
        #     c = tf.feature_column.numeric_column("Price-RA3-" + str(i))
        #     featureColumns.append(c)

        # print(featureColumns)

        # Convert the list of feature columns into a layer that will later be fed into
        # the model.
        featureLayer = layers.DenseFeatures(featureColumns)
        layerParameters = [
            LayerParameter(25, "sigmoid"),
            LayerParameter(4, "sigmoid"),
            LayerParameter(2, "sigmoid"),
        ]

        self.createModel(featureLayer, layerParameters)

    def setupUsingDefaults(self):
        # Hyperparameters!
        learningRate = 0.008
        epochs = 1500
        batchSize = 30
        classificationThreshold = 0.95
        self.setup(classificationThreshold,
                    Hyperparameters(learningRate, epochs,
                                    batchSize))

    def _buildMetrics(self):
        self._metrics = [
            tf.keras.metrics.BinaryAccuracy(name='accuracy',
                                            threshold=self._classificationThreshold),
            tf.keras.metrics.Precision(thresholds=self._classificationThreshold,
                                     name='precision'
                                     ),
            tf.keras.metrics.Recall(thresholds=self._classificationThreshold,
                                  name="recall"),
            tf.keras.metrics.AUC(num_thresholds=100, name='auc')
        ]
        self.listOfMetrics = ["accuracy", "precision", "recall", "auc"]

    def prepareForUse(self):
        """
        Makes sure this model is ready to be used for predictions.
        """
        # We need to tell the model to make a test prediction so that all of
        # the additional GPU DLLs get loaded. Think of it as a warm up :P
        lst = [x / CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES for x in range(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES * 2)]
        self.detect(lst, lst)

    def _turnListOfFloatsToInputData(self, data: List[float], volumeAmount: int, priceAmount: int) -> Dict:
        features = {}
        j = 0

        for i in range(volumeAmount):
            features["Volume-RA-" + str(i)] = np.array(np.float32(data[j]))
            # features["Volume-RA-" + str(i)] = [data[j]]
            j += 1

        for i in range(priceAmount):
            features["Price-RA-" + str(i)] = np.array(np.float32(data[j]))
            # features["Price-RA-" + str(i)] = [data[j]]
            j += 1

        # for i in range(volumeAmount // 2):
        #     features["Volume-RA2-" + str(i)] = np.array(np.float32(data[j]))
        #     # features["Volume-RA-" + str(i)] = [data[j]]
        #     j += 1
        #
        # for i in range(priceAmount // 2):
        #     features["Price-RA2-" + str(i)] = np.array(np.float32(data[j]))
        #     # features["Price-RA-" + str(i)] = [data[j]]
        #     j += 1
        #
        # for i in range(volumeAmount // 3):
        #     features["Volume-RA3-" + str(i)] = np.array(np.float32(data[j]))
        #     # features["Volume-RA-" + str(i)] = [data[j]]
        #     j += 1
        #
        # for i in range(priceAmount // 3):
        #     features["Price-RA3-" + str(i)] = np.array(np.float32(data[j]))
        #     # features["Price-RA-" + str(i)] = [data[j]]
        #     j += 1

        return features

    def _configureForGPU(self):
        # https://www.tensorflow.org/guide/gpu
        gpus = tf.config.experimental.list_physical_devices('GPU')
        if gpus:
            try:
                # Currently, memory growth needs to be the same across GPUs
                for gpu in gpus:
                    tf.config.experimental.set_memory_growth(gpu, True)
                logical_gpus = tf.config.experimental.list_logical_devices(
                    'GPU')
                print(len(gpus), "Physical GPUs,", len(logical_gpus),
                      "Logical GPUs")
            except RuntimeError as e:
                # Memory growth must be set before GPUs have been initialized
                print("CryptoPumpAndDumpDetector GPU setup error: " + str(e))
