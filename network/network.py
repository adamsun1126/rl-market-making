import tensorflow as tf
from tensorflow import keras
from keras import layers, models, regularizers
import numpy as np

# The create_cnn_policy_network function creates a convolutional neural network (CNN) policy network.
# This will determine the actions to take based on the current state.
def create_cnn_attention_policy_network(input_shape):
    model = models.Sequential()
    # First Conv Layer with BatchNormalization
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Conv1D(64, kernel_size=3, activation='relu',  kernel_initializer='he_uniform'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling1D(pool_size=2))
    
    # Second Conv Layer with BatchNormalization
    model.add(layers.Conv1D(128, kernel_size=3, activation='relu', kernel_initializer='he_uniform'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling1D(pool_size=2))
    
    # Third Conv Layer with BatchNormalization (Optional, use if data is complex)
    model.add(layers.Conv1D(256, kernel_size=3, activation='relu', kernel_initializer='he_uniform'))
    model.add(layers.BatchNormalization())
    
    # Flattening
    model.add(layers.Flatten())
    
    # Fully Connected Layers with Dropout
    model.add(layers.Dense(256, activation='relu', kernel_initializer='he_uniform'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(128, activation='relu', kernel_initializer='he_uniform'))
    model.add(layers.Dropout(0.2))
    
    # Output Layer
    model.add(layers.Dense(2, activation='tanh', kernel_initializer='GlorotUniform'))  # Output layer for actions
    
    return model


# The create_cnn_value_network function creates a CNN value network.
# This will estimate the value of the current state.
def create_cnn_attention_value_network(input_shape):
    model = models.Sequential()
    # First Conv Layer with BatchNormalization
    model.add(layers.Input(shape=input_shape))
    model.add(layers.Conv1D(64, kernel_size=3, activation='relu', kernel_initializer='he_normal'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling1D(pool_size=2))
    
    # Second Conv Layer with BatchNormalization
    model.add(layers.Conv1D(128, kernel_size=3, activation='relu', kernel_initializer='he_normal'))
    model.add(layers.BatchNormalization())
    model.add(layers.MaxPooling1D(pool_size=2))
    
    # Third Conv Layer with BatchNormalization (Optional)
    model.add(layers.Conv1D(256, kernel_size=3, activation='relu', kernel_initializer='he_normal'))
    model.add(layers.BatchNormalization())
    
    # Flattening
    model.add(layers.Flatten())
    
    # Fully Connected Layers with Dropout
    model.add(layers.Dense(256, activation='relu', kernel_initializer='he_normal'))
    model.add(layers.Dropout(0.2))
    model.add(layers.Dense(128, activation='relu', kernel_initializer='he_normal'))
    model.add(layers.Dropout(0.2))
    
    # Output Layer
    model.add(layers.Dense(1, activation='linear', kernel_initializer='he_uniform'))  # Single output for value estimation
    
    return model

# LSTM-based policy and value networks for EXPERIMENTATION AND RESEARCH purposes
def create_lstm_policy_network(input_shape, lstm_units=64, output_units=2):
    model = models.Sequential([
        layers.LSTM(lstm_units, return_sequences=True, input_shape=input_shape),
        layers.Dropout(0.2),
        layers.LSTM(lstm_units, return_sequences=False),
        layers.Dropout(0.2),
        layers.Dense(25, activation='relu', kernel_regularizer=regularizers.l2(0.01), kernel_initializer='he_normal'),
        layers.Dense(output_units, activation='sigmoid', kernel_initializer='GlorotUniform')  # Output layer for actions
    ])
    return model

def create_lstm_value_network(input_shape, lstm_units=64):
    model = models.Sequential([
        layers.LSTM(lstm_units, return_sequences=True, input_shape=input_shape),
        layers.Dropout(0.2),
        layers.LSTM(lstm_units, return_sequences=False),
        layers.Dropout(0.2),
        layers.Dense(25, activation='relu', kernel_regularizer=regularizers.l2(0.01), kernel_initializer='he_normal'),
        layers.Dense(1, activation='linear')  # Output a continuous value for the state or state-action value
    ])
    return model