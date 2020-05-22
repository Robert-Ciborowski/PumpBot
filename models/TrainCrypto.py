def train():
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from tensorflow.keras import layers

    from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
    from models.Hyperparameters import Hyperparameters
    from models.LayerParameter import LayerParameter

    print("Loading dataset...")
    pumps_df = pd.read_csv("../data_set/OAXBTC-YOYOBTC-pumps.csv")
    non_pumps_df = pd.read_csv("../data_set/OAXBTC-YOYOBTC-non-pumps.csv")
    all_df = pumps_df.append(non_pumps_df).reset_index(drop=True)
    all_df = all_df.reindex(
        np.random.permutation(all_df.index))
    numberOfEntries = len(all_df.index)
    train_df = all_df.head(int(numberOfEntries * 0.7))

    test_df = all_df.tail(int(numberOfEntries * 0.3))

    # This creates an empty list that will eventually hold all created
    # feature columns.
    featureColumns = []

    for column in all_df.columns:
        if column == "Pump":
            continue

        # Create a numerical feature column to represent the column.
        c = tf.feature_column.numeric_column(column)
        featureColumns.append(c)

    # Convert the list of feature columns into a layer that will later be fed into
    # the model.
    featureLayer = layers.DenseFeatures(featureColumns)

    # Hyperparameters!
    learningRate = 0.008
    epochs = 500
    batchSize = 30
    labelName = "Pump"
    classificationThreshold = 0.5

    model = CryptoPumpAndDumpDetector()
    model.setup(classificationThreshold,
                Hyperparameters(learningRate, epochs,
                                batchSize))
    layerParameters = [
        LayerParameter(5, "sigmoid")
    ]

    model.createModel(featureLayer, layerParameters)
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
