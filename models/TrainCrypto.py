def train():
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from tensorflow.keras import layers

    from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
    from models.Hyperparameters import Hyperparameters
    from models.LayerParameter import LayerParameter

    print("Loading dataset...")
    pumps_df = pd.read_csv("../data_set/final-dataset-pumps.csv")
    non_pumps_df = pd.read_csv("../data_set/final-dataset-non-pumps.csv")
    all_df = pumps_df.append(non_pumps_df).reset_index(drop=True)
    all_df = all_df.reindex(
        np.random.permutation(all_df.index))
    numberOfEntries = len(all_df.index)
    train_df = all_df.head(int(numberOfEntries * 0.7))
    test_df = all_df.tail(int(numberOfEntries * 0.3))

    # Hyperparameters!
    learningRate = 0.025
    epochs = 500
    batchSize = 45
    labelName = "Pump"
    classificationThreshold = 0.75

    model = CryptoPumpAndDumpDetector()
    model.setup(classificationThreshold,
                Hyperparameters(learningRate, epochs,
                                batchSize))

    model.createModelUsingDefaults()
    epochs, hist = model.trainModel(train_df, labelName)
    list_of_metrics_to_plot = model.listOfMetrics
    model.plotCurve(epochs, hist, list_of_metrics_to_plot)

    features = {name: np.array(value) for name, value in test_df.items()}
    label = np.array(features.pop(labelName))

    print(model.evaluate(features, label))

    print("====== Predictions =======")
    # You can do this and things will still work.
    # test_df.pop("Pump")
    print(model.detect(test_df))
    model.exportWeights()


if __name__ == "__main__":
    train()
