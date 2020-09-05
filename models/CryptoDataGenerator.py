from typing import List

import tensorflow as tf
import pandas as pd
import numpy as np

class DataGenerator(tf.keras.utils.Sequence):
    def __init__(self, dataframe: pd.DataFrame, batch_size=32):
        self.batch_size = batch_size
        self.df = dataframe
        self.indices = self.df.index.tolist()
        self.on_epoch_end()

    def __len__(self):
        return len(self.indices) // self.batch_size

    def __getitem__(self, index):
        index = self.indices[
                index * self.batch_size:(index + 1) * self.batch_size]
        X, y = self.__get_data(index)
        return X, y

    def on_epoch_end(self):
        # self.indices = np.arange(len(self.indices))
        np.random.shuffle(self.indices)

    def __get_data(self, index: List):
        X =  # logic
        y =  # logic

        for i, id in enumerate(batch):
            X[i,] =  # logic
            y[i] =  # labels

        return X, y










from keras.layers import Conv1D, Dense, Dropout, Input, Concatenate, GlobalMaxPooling1D
from keras.models import Model#this base model is one branch of the main model
#it takes a time series as an input, performs 1-D convolution, and returns it as an output ready for concatenationdef get_base_model(input_len, fsize):
#the input is a time series of length n and width 19
input_seq = Input(shape=(input_len, 19))
#choose the number of convolution filters
nb_filters = 10
#1-D convolution and global max-pooling
convolved = Conv1D(nb_filters, fsize, padding="same", activation="tanh")(input_seq)
processed = GlobalMaxPooling1D()(convolved)
#dense layer with dropout regularization
compressed = Dense(50, activation="tanh")(processed)
compressed = Dropout(0.3)(compressed)
model = Model(inputs=input_seq, outputs=compressed)
return model#this is the main model
#it takes the original time series and its down-sampled versions as an input, and returns the result of classification as an outputdef main_model(inputs_lens = [512, 1024, 3480], fsizes = [8,16,24]):
#the inputs to the branches are the original time series, and its down-sampled versions
input_smallseq = Input(shape=(inputs_lens[0], 19))
input_medseq = Input(shape=(inputs_lens[1] , 19))
input_origseq = Input(shape=(inputs_lens[2], 19))#the more down-sampled the time series, the shorter the corresponding filter
base_net_small = get_base_model(inputs_lens[0], fsizes[0])
base_net_med = get_base_model(inputs_lens[1], fsizes[1])
base_net_original = get_base_model(inputs_lens[2], fsizes[2])embedding_small = base_net_small(input_smallseq)
embedding_med = base_net_med(input_medseq)
embedding_original = base_net_original(input_origseq)#concatenate all the outputs
merged = Concatenate()([embedding_small, embedding_med, embedding_original])
out = Dense(1, activation='sigmoid')(merged)model = Model(inputs=[input_smallseq, input_medseq, input_origseq], outputs=out)
return model
