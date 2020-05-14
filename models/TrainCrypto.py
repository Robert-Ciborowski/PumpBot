def train():
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from tensorflow.keras import layers

    from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
    from models.Hyperparameters import Hyperparameters
    from models.LayerParameter import LayerParameter

    # The following lines adjust the granularity of reporting.
    pd.options.display.max_rows = 10
    pd.options.display.float_format = "{:.1f}".format
    # tf.keras.backend.set_floatx('float32')

    print("Ran the import statements.")

    # The following lines adjust the granularity of reporting.
    pd.options.display.max_rows = 10
    pd.options.display.float_format = "{:.1f}".format
    # tf.keras.backend.set_floatx('float32')

    print("Ran the import statements.")

    pumps_df = pd.read_csv("../data_set/OAXBTC-YOYOBTC-pumps.csv")
    non_pumps_df = pd.read_csv("../data_set/OAXBTC-YOYOBTC-non-pumps.csv")
    all_df = pumps_df.append(non_pumps_df).reset_index(drop=True)
    print(all_df)
    all_df = all_df.reindex(
        np.random.permutation(all_df.index))
    print(all_df)
    numberOfEntries = len(all_df.index)
    print(numberOfEntries)
    train_df = all_df.head(int(numberOfEntries * 0.7))
    print("TRAIN DF")
    print(train_df)

    test_df = all_df.tail(int(numberOfEntries * 0.3))
    print("TEST DF")
    print(test_df)
    # Create an empty list that will eventually hold all created feature columns.
    featureColumns = []

    count = 0
    for column in all_df.columns:
        if column == "Pump":
            continue

        # Create a numerical feature column to represent the column.
        print("'" + column + "'")
        # c = tf.feature_column.numeric_column("Price-RA-" + str(count))
        c = tf.feature_column.numeric_column(column)
        featureColumns.append(c)
        count += 1

    # Convert the list of feature columns into a layer that will later be fed into
    # the model.
    featureLayer = layers.DenseFeatures(featureColumns)

    # Hyperparameters!
    learningRate = 0.03
    epochs = 1000
    batchSize = 15
    labelName = "Pump"
    classificationThreshold = 0.7

    model = CryptoPumpAndDumpDetector(classificationThreshold,
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
    # print(model.model.predict(test_df[0:5], verbose=1))

if __name__ == "__main__":
    train()
