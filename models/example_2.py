# Example of how to load a model.
if __name__ == "__main__":
    import numpy as np
    import pandas as pd
    import tensorflow as tf
    from tensorflow.keras import layers

    from models.CryptoPumpAndDumpDetector import CryptoPumpAndDumpDetector
    from models.Hyperparameters import Hyperparameters
    from models.LayerParameter import LayerParameter

    model = CryptoPumpAndDumpDetector()
    model.setupUsingDefaults()
    model.createModelUsingDefaults()
    model.loadWeights()
    tester2 = {'Volume-RA-0': -1.4869098102730396,
               'Volume-RA-1': -1.4869098102730396,
               'Volume-RA-2': -1.4869098102730396,
               'Volume-RA-3': -1.4869098102730396,
               'Volume-RA-4': -1.4869098102730396,
               'Volume-RA-5': -1.4869098102730396,
               'Volume-RA-6': -1.4869098102730396,
               'Volume-RA-7': 1.5823522362441633,
               'Volume-RA-8': 1.241323119964474,
               'Volume-RA-9': 0.9684998269407228,
               'Volume-RA-10': 0.7452807690121988,
               'Volume-RA-11': 0.5592648874050954,
               'Volume-RA-12': 0.4018668337375468,
               'Volume-RA-13': 0.266954216308219,
               'Volume-RA-14': 0.1500299478694685,
               'Volume-RA-15': 0.6232078467075373,
               'Volume-RA-16': 0.6796281049155742,
               'Volume-RA-17': 0.7297794455449401,
               'Volume-RA-18': 0.6131115899755728,
               'Volume-RA-19': 0.5081105199631423,
               'Volume-RA-20': 0.4131095518566574,
               'Volume-RA-21': 0.32674503539621663,
               'Volume-RA-22': 0.24789047688885746,
               'Volume-RA-23': 0.17560713159044508,
               'Volume-RA-24': 0.17560713159044508,
               'Price-RA-0': 1.419816230104309,
               'Price-RA-1': 1.419816230104309,
               'Price-RA-2': 1.419816230104309,
               'Price-RA-3': 1.419816230104309,
               'Price-RA-4': 1.419816230104309,
               'Price-RA-5': 1.419816230104309,
               'Price-RA-6': 1.419816230104309,
               'Price-RA-7': 0.8355506561016184,
               'Price-RA-8': 0.38112187632176064,
               'Price-RA-9': 0.017578852497919746,
               'Price-RA-10': -0.2798654397215453,
               'Price-RA-11': -0.5277356832378416,
               'Price-RA-12': -0.7374720431362636,
               'Price-RA-13': -0.9172460659062264,
               'Price-RA-14': -1.0730502189737159,
               'Price-RA-15': -0.9589793211922216,
               'Price-RA-16': -1.0547203186128815,
               'Price-RA-17': -0.9543422928271488,
               'Price-RA-18': -0.8645303750188736,
               'Price-RA-19': -0.7836996489914938,
               'Price-RA-20': -0.7105670873475447,
               'Price-RA-21': -0.6440829403986029,
               'Price-RA-22': -0.5833800236191687,
               'Price-RA-23': -0.5277356832379547,
               'Price-RA-24': -0.5555578534285052}
    print(model.detect(pd.Series(tester2)))
