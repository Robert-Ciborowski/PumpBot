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
    epochs = 50
    batchSize = 300
    labelName = "Pump"
    classificationThreshold = 0.75

    model = CryptoPumpAndDumpDetector(tryUsingGPU=False)
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

    print(test_df.iloc[0])

    tester = {'Volume-RA-0': [-0.29340664], 'Volume-RA-1': [0.38819954], 'Volume-RA-2': [-0.29340664], 'Volume-RA-3': [-0.29340664], 'Volume-RA-4': [-0.29340664], 'Volume-RA-5': [-0.29340664], 'Volume-RA-6': [0.38819954], 'Volume-RA-7': [-0.29340664], 'Volume-RA-8': [-0.29340664], 'Volume-RA-9': [-0.29340664], 'Volume-RA-10': [-0.29340664], 'Volume-RA-11': [0.38819954], 'Volume-RA-12': [-0.29340664], 'Volume-RA-13': [-0.29340664], 'Volume-RA-14': [2.433018], 'Volume-RA-15': [-0.29340664], 'Volume-RA-16': [-0.29340664], 'Volume-RA-17': [-0.29340664], 'Volume-RA-18': [-0.29340664], 'Volume-RA-19': [-0.29340664], 'Volume-RA-20': [-0.29340664], 'Volume-RA-21': [-0.29340664], 'Volume-RA-22': [-0.29340664], 'Volume-RA-23': [-0.29340664], 'Volume-RA-24': [-0.29340664], 'Volume-RA-25': [-0.29340664], 'Volume-RA-26': [-0.29340664], 'Volume-RA-27': [-0.29340664], 'Volume-RA-28': [0.38819954], 'Volume-RA-29': [-0.29340664], 'Volume-RA-30': [-0.29340664], 'Volume-RA-31': [-0.29340664], 'Volume-RA-32': [-0.29340664], 'Volume-RA-33': [-0.29340664], 'Volume-RA-34': [-0.29340664], 'Volume-RA-35': [-0.29340664], 'Volume-RA-36': [-0.29340664], 'Volume-RA-37': [-0.29340664], 'Volume-RA-38': [-0.29340664], 'Volume-RA-39': [-0.29340664], 'Volume-RA-40': [-0.29340664], 'Volume-RA-41': [-0.29340664], 'Volume-RA-42': [1.0698057], 'Volume-RA-43': [0.38819954], 'Volume-RA-44': [-0.29340664], 'Volume-RA-45': [-0.29340664], 'Volume-RA-46': [1.7514119], 'Volume-RA-47': [-0.29340664], 'Volume-RA-48': [-0.29340664], 'Volume-RA-49': [-0.29340664], 'Volume-RA-50': [-0.29340664], 'Volume-RA-51': [1.7514119], 'Volume-RA-52': [-0.29340664], 'Volume-RA-53': [-0.29340664], 'Volume-RA-54': [0.38819954], 'Volume-RA-55': [-0.29340664], 'Volume-RA-56': [-0.29340664], 'Volume-RA-57': [-0.29340664], 'Volume-RA-58': [-0.29340664], 'Volume-RA-59': [-0.29340664], 'Volume-RA-60': [5.841049], 'Volume-RA-61': [0.38819954], 'Volume-RA-62': [-0.29340664], 'Volume-RA-63': [-0.29340664], 'Volume-RA-64': [-0.29340664], 'Volume-RA-65': [-0.29340664], 'Volume-RA-66': [3.7962306], 'Volume-RA-67': [-0.29340664], 'Volume-RA-68': [-0.29340664], 'Volume-RA-69': [-0.29340664], 'Volume-RA-70': [-0.29340664], 'Volume-RA-71': [-0.29340664], 'Volume-RA-72': [-0.29340664], 'Volume-RA-73': [-0.29340664], 'Volume-RA-74': [-0.29340664], 'Volume-RA-75': [-0.29340664], 'Volume-RA-76': [-0.29340664], 'Volume-RA-77': [-0.29340664], 'Volume-RA-78': [-0.29340664], 'Volume-RA-79': [-0.29340664], 'Volume-RA-80': [-0.29340664], 'Volume-RA-81': [-0.29340664], 'Volume-RA-82': [-0.29340664], 'Volume-RA-83': [-0.29340664], 'Volume-RA-84': [-0.29340664], 'Volume-RA-85': [2.433018], 'Volume-RA-86': [-0.29340664], 'Volume-RA-87': [-0.29340664], 'Volume-RA-88': [-0.29340664], 'Volume-RA-89': [0.38819954], 'Volume-RA-90': [-0.29340664], 'Volume-RA-91': [-0.29340664], 'Volume-RA-92': [-0.29340664], 'Volume-RA-93': [1.7514119], 'Volume-RA-94': [-0.29340664], 'Volume-RA-95': [-0.29340664], 'Volume-RA-96': [0.38819954], 'Volume-RA-97': [-0.29340664], 'Volume-RA-98': [-0.29340664], 'Volume-RA-99': [-0.29340664], 'Volume-RA-100': [-0.29340664], 'Volume-RA-101': [-0.29340664], 'Volume-RA-102': [-0.29340664], 'Volume-RA-103': [-0.29340664], 'Volume-RA-104': [-0.29340664], 'Volume-RA-105': [-0.29340664], 'Volume-RA-106': [-0.29340664], 'Volume-RA-107': [-0.29340664], 'Volume-RA-108': [-0.29340664], 'Volume-RA-109': [-0.29340664], 'Volume-RA-110': [-0.29340664], 'Volume-RA-111': [1.7514119], 'Volume-RA-112': [1.0698057], 'Volume-RA-113': [-0.29340664], 'Volume-RA-114': [-0.29340664], 'Volume-RA-115': [-0.29340664], 'Volume-RA-116': [0.38819954], 'Volume-RA-117': [0.38819954], 'Volume-RA-118': [-0.29340664], 'Volume-RA-119': [-0.29340664], 'Volume-RA-120': [-0.29340664], 'Volume-RA-121': [0.38819954], 'Volume-RA-122': [-0.29340664], 'Volume-RA-123': [-0.29340664], 'Volume-RA-124': [-0.29340664], 'Volume-RA-125': [-0.29340664], 'Volume-RA-126': [-0.29340664], 'Volume-RA-127': [-0.29340664], 'Volume-RA-128': [-0.29340664], 'Volume-RA-129': [-0.29340664], 'Volume-RA-130': [-0.29340664], 'Volume-RA-131': [-0.29340664], 'Volume-RA-132': [-0.29340664], 'Volume-RA-133': [-0.29340664], 'Volume-RA-134': [-0.29340664], 'Volume-RA-135': [-0.29340664], 'Volume-RA-136': [-0.29340664], 'Volume-RA-137': [-0.29340664], 'Volume-RA-138': [1.0698057], 'Volume-RA-139': [7.8858676], 'Volume-RA-140': [-0.29340664], 'Volume-RA-141': [-0.29340664], 'Volume-RA-142': [-0.29340664], 'Volume-RA-143': [-0.29340664], 'Volume-RA-144': [-0.29340664], 'Volume-RA-145': [-0.29340664], 'Volume-RA-146': [-0.29340664], 'Volume-RA-147': [-0.29340664], 'Volume-RA-148': [-0.29340664], 'Volume-RA-149': [-0.29340664], 'Price-RA-0': [-0.29340664], 'Price-RA-1': [-1.4002801], 'Price-RA-2': [0.361739], 'Price-RA-3': [0.361739], 'Price-RA-4': [0.361739], 'Price-RA-5': [0.361739], 'Price-RA-6': [0.361739], 'Price-RA-7': [2.123758], 'Price-RA-8': [2.123758], 'Price-RA-9': [2.123758], 'Price-RA-10': [2.123758], 'Price-RA-11': [2.123758], 'Price-RA-12': [0.361739], 'Price-RA-13': [0.361739], 'Price-RA-14': [0.361739], 'Price-RA-15': [0.361739], 'Price-RA-16': [0.361739], 'Price-RA-17': [0.361739], 'Price-RA-18': [0.361739], 'Price-RA-19': [0.361739], 'Price-RA-20': [0.361739], 'Price-RA-21': [0.361739], 'Price-RA-22': [0.361739], 'Price-RA-23': [0.361739], 'Price-RA-24': [0.361739], 'Price-RA-25': [0.361739], 'Price-RA-26': [0.361739], 'Price-RA-27': [0.361739], 'Price-RA-28': [0.361739], 'Price-RA-29': [0.361739], 'Price-RA-30': [0.361739], 'Price-RA-31': [0.361739], 'Price-RA-32': [0.361739], 'Price-RA-33': [0.361739], 'Price-RA-34': [0.361739], 'Price-RA-35': [0.361739], 'Price-RA-36': [0.361739], 'Price-RA-37': [0.361739], 'Price-RA-38': [0.361739], 'Price-RA-39': [0.361739], 'Price-RA-40': [0.361739], 'Price-RA-41': [0.361739], 'Price-RA-42': [0.361739], 'Price-RA-43': [0.361739], 'Price-RA-44': [0.361739], 'Price-RA-45': [0.361739], 'Price-RA-46': [0.361739], 'Price-RA-47': [0.361739], 'Price-RA-48': [0.361739], 'Price-RA-49': [0.361739], 'Price-RA-50': [0.361739], 'Price-RA-51': [0.361739], 'Price-RA-52': [-1.4002801], 'Price-RA-53': [-1.4002801], 'Price-RA-54': [-1.4002801], 'Price-RA-55': [-1.4002801], 'Price-RA-56': [-1.4002801], 'Price-RA-57': [-1.4002801], 'Price-RA-58': [-1.4002801], 'Price-RA-59': [-1.4002801], 'Price-RA-60': [-1.4002801], 'Price-RA-61': [3.8857772], 'Price-RA-62': [-1.4002801], 'Price-RA-63': [-1.4002801], 'Price-RA-64': [-1.4002801], 'Price-RA-65': [-1.4002801], 'Price-RA-66': [-1.4002801], 'Price-RA-67': [-1.4002801], 'Price-RA-68': [-1.4002801], 'Price-RA-69': [-1.4002801], 'Price-RA-70': [-1.4002801], 'Price-RA-71': [-1.4002801], 'Price-RA-72': [-1.4002801], 'Price-RA-73': [-1.4002801], 'Price-RA-74': [-1.4002801], 'Price-RA-75': [-1.4002801], 'Price-RA-76': [-1.4002801], 'Price-RA-77': [-1.4002801], 'Price-RA-78': [-1.4002801], 'Price-RA-79': [-1.4002801], 'Price-RA-80': [-1.4002801], 'Price-RA-81': [-1.4002801], 'Price-RA-82': [-1.4002801], 'Price-RA-83': [-1.4002801], 'Price-RA-84': [-1.4002801], 'Price-RA-85': [-1.4002801], 'Price-RA-86': [-1.4002801], 'Price-RA-87': [-1.4002801], 'Price-RA-88': [-1.4002801], 'Price-RA-89': [-1.4002801], 'Price-RA-90': [-1.4002801], 'Price-RA-91': [-1.4002801], 'Price-RA-92': [-1.4002801], 'Price-RA-93': [-1.4002801], 'Price-RA-94': [2.123758], 'Price-RA-95': [2.123758], 'Price-RA-96': [2.123758], 'Price-RA-97': [0.361739], 'Price-RA-98': [0.361739], 'Price-RA-99': [0.361739], 'Price-RA-100': [0.361739], 'Price-RA-101': [0.361739], 'Price-RA-102': [0.361739], 'Price-RA-103': [0.361739], 'Price-RA-104': [0.361739], 'Price-RA-105': [0.361739], 'Price-RA-106': [0.361739], 'Price-RA-107': [0.361739], 'Price-RA-108': [0.361739], 'Price-RA-109': [0.361739], 'Price-RA-110': [0.361739], 'Price-RA-111': [0.361739], 'Price-RA-112': [2.123758], 'Price-RA-113': [0.361739], 'Price-RA-114': [0.361739], 'Price-RA-115': [0.361739], 'Price-RA-116': [0.361739], 'Price-RA-117': [0.361739], 'Price-RA-118': [0.361739], 'Price-RA-119': [0.361739], 'Price-RA-120': [0.361739], 'Price-RA-121': [0.361739], 'Price-RA-122': [0.361739], 'Price-RA-123': [0.361739], 'Price-RA-124': [0.361739], 'Price-RA-125': [0.361739], 'Price-RA-126': [0.361739], 'Price-RA-127': [0.361739], 'Price-RA-128': [0.361739], 'Price-RA-129': [0.361739], 'Price-RA-130': [0.361739], 'Price-RA-131': [0.361739], 'Price-RA-132': [0.361739], 'Price-RA-133': [0.361739], 'Price-RA-134': [0.361739], 'Price-RA-135': [0.361739], 'Price-RA-136': [0.361739], 'Price-RA-137': [0.361739], 'Price-RA-138': [0.361739], 'Price-RA-139': [0.361739], 'Price-RA-140': [0.361739], 'Price-RA-141': [0.361739], 'Price-RA-142': [0.361739], 'Price-RA-143': [0.361739], 'Price-RA-144': [0.361739], 'Price-RA-145': [0.361739], 'Price-RA-146': [0.361739], 'Price-RA-147': [0.361739], 'Price-RA-148': [0.361739], 'Price-RA-149': [0.361739]}
    model.detect(tester)

    print("====== Predictions =======")
    model.exportWeights()


if __name__ == "__main__":
    train()
