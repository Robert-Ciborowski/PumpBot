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

from models.LayerParameter import LayerParameter
from models.Hyperparameters import Hyperparameters
from models.PumpAndDumpDetector import PumpAndDumpDetector
from thread_runner.ThreadRunner import ThreadRunner
from util.Constants import MINUTES_OF_DATA_TO_LOOK_AT
import threading as th


class CryptoPumpAndDumpDetector(PumpAndDumpDetector):
    hyperparameters: Hyperparameters
    listOfMetrics: List
    exportPath: str
    threadRunner: ThreadRunner

    _runThread: th.Thread
    _metrics: List
    _NUMBER_OF_SAMPLES = MINUTES_OF_DATA_TO_LOOK_AT

    def __init__(self, tryUsingGPU=False, threadRunner=None):
        super().__init__()

        if not tryUsingGPU:
            os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
        else:
            self._configureForGPU()

        self.exportPath = "./model_exports/cryptopumpanddumpdetector"
        self.threadRunner = threadRunner

        # Experimental
        # tf.config.optimizer.set_jit(True)
        # from tensorflow.keras.mixed_precision import \
        #     experimental as mixed_precision
        # policy = mixed_precision.Policy('mixed_float16')
        # mixed_precision.set_policy(policy)

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
    def detect(self, prices) -> bool:
        if isinstance(prices, pd.DataFrame):
            data = {name: np.array(np.float32(value)) for name, value in
                    prices.items()}
        if isinstance(prices, pd.Series):
            data = {name: np.array([np.float32(value)]) for name, value in
                    prices.iteritems()}
        elif isinstance(prices, List) or isinstance(prices, np.ndarray):
            # The list better contain only floats...
            data = self._turnListOfFloatsToInputData(prices)
        elif isinstance(prices, Dict):
            data = prices
        else:
            print("CryptoPumpAndDumpDetector detect() had its precondition "
                  "violated!")
            return False

        if data is None or len(
                data) < CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES * 2:
            print("CryptoPumpAndDumpDetector detect() was not given enough "
                  "data to work with!")
            return False

        # if self.threadRunner is None:
        return self._detect(data)
        # else:
        # f = lambda: self._detect(data)
        # result = self.threadRunner.run(f)
        # print("Cryptopump: " + str(result))
        # return result

    def _detect(self, data):
        data = self._makeTestData()
        time1 = datetime.now()
        # result = self.model.predict(data)[0][0]
        result = self.model(data).numpy()[0][0]
        time2 = datetime.now()
        print("Gave out a result of " + str(result) + ", took " + str(
            time2 - time1))
        return result >= self._classificationThreshold

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
                                            # kernel_regularizer=tf.keras.regularizers.l2(
                                            #     l=0.04),
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

        # Experimental
        # pruning_schedule = tfmot.sparsity.keras.PolynomialDecay(
        #     initial_sparsity=0.0, final_sparsity=0.5,
        #     begin_step=1000, end_step=3000)
        #
        # self.model = tfmot.sparsity.keras.prune_low_magnitude(self.model,
        #                                                              pruning_schedule=pruning_schedule)
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
            LayerParameter(10, "sigmoid"),
            LayerParameter(5, "sigmoid")
        ]

        self.createModel(featureLayer, layerParameters)

    def setupUsingDefaults(self):
        # Hyperparameters!
        learningRate = 0.008
        epochs = 500
        batchSize = 30
        classificationThreshold = 0.7
        self.setup(classificationThreshold,
                    Hyperparameters(learningRate, epochs,
                                    batchSize))

    def _turnListOfFloatsToInputData(self, data: List[float]) -> Dict:
        if len(data) < CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES * 2:
            return None

        features = {}
        j = 0

        for i in range(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES):
            features["Volume-RA-" + str(i)] = np.float32(data[j])
            j += 1

        for i in range(CryptoPumpAndDumpDetector._NUMBER_OF_SAMPLES):
            features["Price-RA-" + str(i)] = np.float32(data[j])
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
            tf.keras.metrics.AUC(num_thresholds=100, name='auc')
        ]
        self.listOfMetrics = ["accuracy", "precision", "recall", "auc"]

    def prepareForUse(self):
        """
        Makes sure this model is ready to be used for predictions.
        """
        # We need to tell the model to make a test prediction so that all of
        # the additional GPU DLLs get loaded. Think of it as a warm up :P
        lst = [np.array([0]) for x in range(self._NUMBER_OF_SAMPLES * 2)]
        self.detect(lst)
        # self.model._make_predict_function()
        # self.graph = tf.get_default_graph()
        # self.graph.finalize()

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

    def _makeTestData(self):
        return {'Volume-RA-0': [-0.29340664], 'Volume-RA-1': [0.38819954],
                  'Volume-RA-2': [-0.29340664], 'Volume-RA-3': [-0.29340664],
                  'Volume-RA-4': [-0.29340664], 'Volume-RA-5': [-0.29340664],
                  'Volume-RA-6': [0.38819954], 'Volume-RA-7': [-0.29340664],
                  'Volume-RA-8': [-0.29340664], 'Volume-RA-9': [-0.29340664],
                  'Volume-RA-10': [-0.29340664], 'Volume-RA-11': [0.38819954],
                  'Volume-RA-12': [-0.29340664], 'Volume-RA-13': [-0.29340664],
                  'Volume-RA-14': [2.433018], 'Volume-RA-15': [-0.29340664],
                  'Volume-RA-16': [-0.29340664], 'Volume-RA-17': [-0.29340664],
                  'Volume-RA-18': [-0.29340664], 'Volume-RA-19': [-0.29340664],
                  'Volume-RA-20': [-0.29340664], 'Volume-RA-21': [-0.29340664],
                  'Volume-RA-22': [-0.29340664], 'Volume-RA-23': [-0.29340664],
                  'Volume-RA-24': [-0.29340664], 'Volume-RA-25': [-0.29340664],
                  'Volume-RA-26': [-0.29340664], 'Volume-RA-27': [-0.29340664],
                  'Volume-RA-28': [0.38819954], 'Volume-RA-29': [-0.29340664],
                  'Volume-RA-30': [-0.29340664], 'Volume-RA-31': [-0.29340664],
                  'Volume-RA-32': [-0.29340664], 'Volume-RA-33': [-0.29340664],
                  'Volume-RA-34': [-0.29340664], 'Volume-RA-35': [-0.29340664],
                  'Volume-RA-36': [-0.29340664], 'Volume-RA-37': [-0.29340664],
                  'Volume-RA-38': [-0.29340664], 'Volume-RA-39': [-0.29340664],
                  'Volume-RA-40': [-0.29340664], 'Volume-RA-41': [-0.29340664],
                  'Volume-RA-42': [1.0698057], 'Volume-RA-43': [0.38819954],
                  'Volume-RA-44': [-0.29340664], 'Volume-RA-45': [-0.29340664],
                  'Volume-RA-46': [1.7514119], 'Volume-RA-47': [-0.29340664],
                  'Volume-RA-48': [-0.29340664], 'Volume-RA-49': [-0.29340664],
                  'Volume-RA-50': [-0.29340664], 'Volume-RA-51': [1.7514119],
                  'Volume-RA-52': [-0.29340664], 'Volume-RA-53': [-0.29340664],
                  'Volume-RA-54': [0.38819954], 'Volume-RA-55': [-0.29340664],
                  'Volume-RA-56': [-0.29340664], 'Volume-RA-57': [-0.29340664],
                  'Volume-RA-58': [-0.29340664], 'Volume-RA-59': [-0.29340664],
                  'Volume-RA-60': [5.841049], 'Volume-RA-61': [0.38819954],
                  'Volume-RA-62': [-0.29340664], 'Volume-RA-63': [-0.29340664],
                  'Volume-RA-64': [-0.29340664], 'Volume-RA-65': [-0.29340664],
                  'Volume-RA-66': [3.7962306], 'Volume-RA-67': [-0.29340664],
                  'Volume-RA-68': [-0.29340664], 'Volume-RA-69': [-0.29340664],
                  'Volume-RA-70': [-0.29340664], 'Volume-RA-71': [-0.29340664],
                  'Volume-RA-72': [-0.29340664], 'Volume-RA-73': [-0.29340664],
                  'Volume-RA-74': [-0.29340664], 'Volume-RA-75': [-0.29340664],
                  'Volume-RA-76': [-0.29340664], 'Volume-RA-77': [-0.29340664],
                  'Volume-RA-78': [-0.29340664], 'Volume-RA-79': [-0.29340664],
                  'Volume-RA-80': [-0.29340664], 'Volume-RA-81': [-0.29340664],
                  'Volume-RA-82': [-0.29340664], 'Volume-RA-83': [-0.29340664],
                  'Volume-RA-84': [-0.29340664], 'Volume-RA-85': [2.433018],
                  'Volume-RA-86': [-0.29340664], 'Volume-RA-87': [-0.29340664],
                  'Volume-RA-88': [-0.29340664], 'Volume-RA-89': [0.38819954],
                  'Volume-RA-90': [-0.29340664], 'Volume-RA-91': [-0.29340664],
                  'Volume-RA-92': [-0.29340664], 'Volume-RA-93': [1.7514119],
                  'Volume-RA-94': [-0.29340664], 'Volume-RA-95': [-0.29340664],
                  'Volume-RA-96': [0.38819954], 'Volume-RA-97': [-0.29340664],
                  'Volume-RA-98': [-0.29340664], 'Volume-RA-99': [-0.29340664],
                  'Volume-RA-100': [-0.29340664],
                  'Volume-RA-101': [-0.29340664],
                  'Volume-RA-102': [-0.29340664],
                  'Volume-RA-103': [-0.29340664],
                  'Volume-RA-104': [-0.29340664],
                  'Volume-RA-105': [-0.29340664],
                  'Volume-RA-106': [-0.29340664],
                  'Volume-RA-107': [-0.29340664],
                  'Volume-RA-108': [-0.29340664],
                  'Volume-RA-109': [-0.29340664],
                  'Volume-RA-110': [-0.29340664], 'Volume-RA-111': [1.7514119],
                  'Volume-RA-112': [1.0698057], 'Volume-RA-113': [-0.29340664],
                  'Volume-RA-114': [-0.29340664],
                  'Volume-RA-115': [-0.29340664], 'Volume-RA-116': [0.38819954],
                  'Volume-RA-117': [0.38819954], 'Volume-RA-118': [-0.29340664],
                  'Volume-RA-119': [-0.29340664],
                  'Volume-RA-120': [-0.29340664], 'Volume-RA-121': [0.38819954],
                  'Volume-RA-122': [-0.29340664],
                  'Volume-RA-123': [-0.29340664],
                  'Volume-RA-124': [-0.29340664],
                  'Volume-RA-125': [-0.29340664],
                  'Volume-RA-126': [-0.29340664],
                  'Volume-RA-127': [-0.29340664],
                  'Volume-RA-128': [-0.29340664],
                  'Volume-RA-129': [-0.29340664],
                  'Volume-RA-130': [-0.29340664],
                  'Volume-RA-131': [-0.29340664],
                  'Volume-RA-132': [-0.29340664],
                  'Volume-RA-133': [-0.29340664],
                  'Volume-RA-134': [-0.29340664],
                  'Volume-RA-135': [-0.29340664],
                  'Volume-RA-136': [-0.29340664],
                  'Volume-RA-137': [-0.29340664], 'Volume-RA-138': [1.0698057],
                  'Volume-RA-139': [7.8858676], 'Volume-RA-140': [-0.29340664],
                  'Volume-RA-141': [-0.29340664],
                  'Volume-RA-142': [-0.29340664],
                  'Volume-RA-143': [-0.29340664],
                  'Volume-RA-144': [-0.29340664],
                  'Volume-RA-145': [-0.29340664],
                  'Volume-RA-146': [-0.29340664],
                  'Volume-RA-147': [-0.29340664],
                  'Volume-RA-148': [-0.29340664],
                  'Volume-RA-149': [-0.29340664], 'Price-RA-0': [-0.29340664],
                  'Price-RA-1': [-1.4002801], 'Price-RA-2': [0.361739],
                  'Price-RA-3': [0.361739], 'Price-RA-4': [0.361739],
                  'Price-RA-5': [0.361739], 'Price-RA-6': [0.361739],
                  'Price-RA-7': [2.123758], 'Price-RA-8': [2.123758],
                  'Price-RA-9': [2.123758], 'Price-RA-10': [2.123758],
                  'Price-RA-11': [2.123758], 'Price-RA-12': [0.361739],
                  'Price-RA-13': [0.361739], 'Price-RA-14': [0.361739],
                  'Price-RA-15': [0.361739], 'Price-RA-16': [0.361739],
                  'Price-RA-17': [0.361739], 'Price-RA-18': [0.361739],
                  'Price-RA-19': [0.361739], 'Price-RA-20': [0.361739],
                  'Price-RA-21': [0.361739], 'Price-RA-22': [0.361739],
                  'Price-RA-23': [0.361739], 'Price-RA-24': [0.361739],
                  'Price-RA-25': [0.361739], 'Price-RA-26': [0.361739],
                  'Price-RA-27': [0.361739], 'Price-RA-28': [0.361739],
                  'Price-RA-29': [0.361739], 'Price-RA-30': [0.361739],
                  'Price-RA-31': [0.361739], 'Price-RA-32': [0.361739],
                  'Price-RA-33': [0.361739], 'Price-RA-34': [0.361739],
                  'Price-RA-35': [0.361739], 'Price-RA-36': [0.361739],
                  'Price-RA-37': [0.361739], 'Price-RA-38': [0.361739],
                  'Price-RA-39': [0.361739], 'Price-RA-40': [0.361739],
                  'Price-RA-41': [0.361739], 'Price-RA-42': [0.361739],
                  'Price-RA-43': [0.361739], 'Price-RA-44': [0.361739],
                  'Price-RA-45': [0.361739], 'Price-RA-46': [0.361739],
                  'Price-RA-47': [0.361739], 'Price-RA-48': [0.361739],
                  'Price-RA-49': [0.361739], 'Price-RA-50': [0.361739],
                  'Price-RA-51': [0.361739], 'Price-RA-52': [-1.4002801],
                  'Price-RA-53': [-1.4002801], 'Price-RA-54': [-1.4002801],
                  'Price-RA-55': [-1.4002801], 'Price-RA-56': [-1.4002801],
                  'Price-RA-57': [-1.4002801], 'Price-RA-58': [-1.4002801],
                  'Price-RA-59': [-1.4002801], 'Price-RA-60': [-1.4002801],
                  'Price-RA-61': [3.8857772], 'Price-RA-62': [-1.4002801],
                  'Price-RA-63': [-1.4002801], 'Price-RA-64': [-1.4002801],
                  'Price-RA-65': [-1.4002801], 'Price-RA-66': [-1.4002801],
                  'Price-RA-67': [-1.4002801], 'Price-RA-68': [-1.4002801],
                  'Price-RA-69': [-1.4002801], 'Price-RA-70': [-1.4002801],
                  'Price-RA-71': [-1.4002801], 'Price-RA-72': [-1.4002801],
                  'Price-RA-73': [-1.4002801], 'Price-RA-74': [-1.4002801],
                  'Price-RA-75': [-1.4002801], 'Price-RA-76': [-1.4002801],
                  'Price-RA-77': [-1.4002801], 'Price-RA-78': [-1.4002801],
                  'Price-RA-79': [-1.4002801], 'Price-RA-80': [-1.4002801],
                  'Price-RA-81': [-1.4002801], 'Price-RA-82': [-1.4002801],
                  'Price-RA-83': [-1.4002801], 'Price-RA-84': [-1.4002801],
                  'Price-RA-85': [-1.4002801], 'Price-RA-86': [-1.4002801],
                  'Price-RA-87': [-1.4002801], 'Price-RA-88': [-1.4002801],
                  'Price-RA-89': [-1.4002801], 'Price-RA-90': [-1.4002801],
                  'Price-RA-91': [-1.4002801], 'Price-RA-92': [-1.4002801],
                  'Price-RA-93': [-1.4002801], 'Price-RA-94': [2.123758],
                  'Price-RA-95': [2.123758], 'Price-RA-96': [2.123758],
                  'Price-RA-97': [0.361739], 'Price-RA-98': [0.361739],
                  'Price-RA-99': [0.361739], 'Price-RA-100': [0.361739],
                  'Price-RA-101': [0.361739], 'Price-RA-102': [0.361739],
                  'Price-RA-103': [0.361739], 'Price-RA-104': [0.361739],
                  'Price-RA-105': [0.361739], 'Price-RA-106': [0.361739],
                  'Price-RA-107': [0.361739], 'Price-RA-108': [0.361739],
                  'Price-RA-109': [0.361739], 'Price-RA-110': [0.361739],
                  'Price-RA-111': [0.361739], 'Price-RA-112': [2.123758],
                  'Price-RA-113': [0.361739], 'Price-RA-114': [0.361739],
                  'Price-RA-115': [0.361739], 'Price-RA-116': [0.361739],
                  'Price-RA-117': [0.361739], 'Price-RA-118': [0.361739],
                  'Price-RA-119': [0.361739], 'Price-RA-120': [0.361739],
                  'Price-RA-121': [0.361739], 'Price-RA-122': [0.361739],
                  'Price-RA-123': [0.361739], 'Price-RA-124': [0.361739],
                  'Price-RA-125': [0.361739], 'Price-RA-126': [0.361739],
                  'Price-RA-127': [0.361739], 'Price-RA-128': [0.361739],
                  'Price-RA-129': [0.361739], 'Price-RA-130': [0.361739],
                  'Price-RA-131': [0.361739], 'Price-RA-132': [0.361739],
                  'Price-RA-133': [0.361739], 'Price-RA-134': [0.361739],
                  'Price-RA-135': [0.361739], 'Price-RA-136': [0.361739],
                  'Price-RA-137': [0.361739], 'Price-RA-138': [0.361739],
                  'Price-RA-139': [0.361739], 'Price-RA-140': [0.361739],
                  'Price-RA-141': [0.361739], 'Price-RA-142': [0.361739],
                  'Price-RA-143': [0.361739], 'Price-RA-144': [0.361739],
                  'Price-RA-145': [0.361739], 'Price-RA-146': [0.361739],
                  'Price-RA-147': [0.361739], 'Price-RA-148': [0.361739],
                  'Price-RA-149': [0.361739]}

