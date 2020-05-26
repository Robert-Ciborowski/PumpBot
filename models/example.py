# Example of how to train a model on a data set. The data set used here is
# the California data set (I got inspired by that one Google TF Crash Course).
if __name__ == "__main__":

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

    train_df = pd.read_csv(
        "https://download.mlcc.google.com/mledu-datasets/california_housing_train.csv")
    test_df = pd.read_csv(
        "https://download.mlcc.google.com/mledu-datasets/california_housing_test.csv")
    train_df = train_df.reindex(
        np.random.permutation(train_df.index))  # shuffle the training set

    # Calculate the Z-scores of each column in the training set and
    # write those Z-scores into a new pandas DataFrame named train_df_norm.
    train_df_mean = train_df.mean()
    train_df_std = train_df.std()
    train_df_norm = (train_df - train_df_mean) / train_df_std

    # Examine some of the values of the normalized training set. Notice that most
    # Z-scores fall between -2 and +2.
    train_df_norm.head()

    # Calculate the Z-scores of each column in the test set and
    # write those Z-scores into a new pandas DataFrame named test_df_norm.
    test_df_mean = test_df.mean()
    test_df_std = test_df.std()
    test_df_norm = (test_df - test_df_mean) / test_df_std

    # @title Double-click for possible solutions.

    # We arbitrarily set the threshold to 265,000, which is
    # the 75th percentile for median house values.  Every neighborhood
    # with a median house price above 265,000 will be labeled 1,
    # and all other neighborhoods will be labeled 0.
    threshold = 265000
    train_df_norm["median_house_value_is_high"] = (
                train_df["median_house_value"] > threshold).astype(float)
    test_df_norm["median_house_value_is_high"] = (
                test_df["median_house_value"] > threshold).astype(float)
    train_df_norm["median_house_value_is_high"].head(8000)

    # Alternatively, instead of picking the threshold
    # based on raw house values, you can work with Z-scores.
    # For example, the following possible solution uses a Z-score
    # of +1.0 as the threshold, meaning that no more
    # than 16% of the values in median_house_value_is_high
    # will be labeled 1.

    # threshold_in_Z = 1.0
    # train_df_norm["median_house_value_is_high"] = (train_df_norm["median_house_value"] > threshold_in_Z).astype(float)
    # test_df_norm["median_house_value_is_high"] = (test_df_norm["median_house_value"] > threshold_in_Z).astype(float)

    # Create an empty list that will eventually hold all created feature columns.
    feature_columns = []

    # Create a numerical feature column to represent median_income.
    median_income = tf.feature_column.numeric_column("median_income")
    feature_columns.append(median_income)

    # Create a numerical feature column to represent total_rooms.
    tr = tf.feature_column.numeric_column("total_rooms")
    feature_columns.append(tr)

    # Convert the list of feature columns into a layer that will later be fed into
    # the model.
    feature_layer = layers.DenseFeatures(feature_columns)

    # Print the first 3 and last 3 rows of the feature_layer's output when applied
    # to train_df_norm:
    feature_layer(dict(train_df_norm))

    # Hyperparameters!
    learningRate = 0.001
    epochs = 20
    batchSize = 100
    labelName = "median_house_value_is_high"
    classificationThreshold = 0.35

    model = CryptoPumpAndDumpDetector()
    model.setup(classificationThreshold,
                Hyperparameters(learningRate, epochs,
                                batchSize))

    layerParameters = [
        # LayerParameter(1, "sigmoid")
    ]

    model.createModel(feature_layer, layerParameters)
    epochs, hist = model.trainModel(train_df_norm, labelName)
    list_of_metrics_to_plot = model.listOfMetrics
    model.plotCurve(epochs, hist, list_of_metrics_to_plot)

    features = {name: np.array(value) for name, value in test_df_norm.items()}
    label = np.array(features.pop(labelName))

    print(model.evaluate(features, label))
