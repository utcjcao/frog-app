import collections
import datetime
import fluidsynth
import glob
import numpy as np
import pathlib
import pandas as pd
import pretty_midi
import seaborn as sns
import tensorflow as tf
import keras_tuner as kt
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import load_data
import variables

load_data.load()
filenames = glob.glob(str(variables.get_data_dir()/'**/*.mid*'))

filenames = filenames[:5]
print('done loading')

# Step 1: Convert MIDI Files to Note Sequences
def midi_to_sequence(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    notes = []
    for instrument in midi_data.instruments:
        if not instrument.is_drum:  # Filter out drum instruments
            notes.extend([note.pitch for note in instrument.notes])
    return notes

# Step 2: Generate Training Sequences from Each File
def prepare_sequences(notes, seq_length):
    sequences = []
    for i in range(len(notes) - seq_length):
        seq_in = notes[i:i+seq_length]
        seq_out = notes[i+seq_length]
        sequences.append((seq_in, seq_out))
    return sequences

# Step 3: Process All MIDI Files and Prepare Input and Target Data
def create_dataset(midi_files, seq_length):
    X = []
    y = []
    for midi_file in tqdm(midi_files, desc='Processing MIDI files'):
        notes = midi_to_sequence(midi_file)
        sequences = prepare_sequences(notes, seq_length)
        for seq_in, seq_out in sequences:
            X.append(seq_in)
            y.append(seq_out)
    return np.array(X), np.array(y)

print('done functions')

# Usage Example
seq_length = 50  # Define the sequence length
X, y = create_dataset(filenames, seq_length)

print('done dataset')

# Step 4: You would now proceed to build your RNN model using X and y as the training data.

def preprocess_data_in_batches(X, y, encoder, batch_size=1000):
    vocab_size = len(encoder.classes_)
    processed_X = []
    processed_y = []
    
    for i in range(0, len(X), batch_size):
        X_batch = X[i:i + batch_size]
        y_batch = y[i:i + batch_size]
        
        X_encoded = [encoder.transform(seq) for seq in X_batch]
        y_encoded = encoder.transform(y_batch)
        
        X_onehot = np.array([to_categorical(seq, num_classes=vocab_size) for seq in X_encoded])
        y_onehot = to_categorical(y_encoded, num_classes=vocab_size)
        
        processed_X.append(X_onehot)
        processed_y.append(y_onehot)
    
    # Concatenate all batches
    return np.concatenate(processed_X), np.concatenate(processed_y), vocab_size



# Usage
# Step 1: Fit the LabelEncoder on the entire dataset
flat_X = [item for sublist in X for item in sublist]  # Flatten the list of sequences
flat_y = [item for item in y]  # Flatten y if necessary
encoder = LabelEncoder()
encoder.fit(flat_X + flat_y)  # Fit the encoder on the entire dataset

# Step 2: Preprocess data in batches
batch_size = 1000  # Adjust this based on your available RAM
X, y, vocab_size = preprocess_data_in_batches(X, y, encoder, batch_size)

print('done preprocess')



def build_model(seq_length, vocab_size):
    model = Sequential()
    model.add(LSTM(128, input_shape=(seq_length, vocab_size), return_sequences=True))
    model.add(Dropout(0.2))
    model.add(LSTM(128))
    model.add(Dropout(0.2))
    model.add(Dense(vocab_size, activation='softmax'))  # Output layer for classification
    return model

model = build_model(seq_length, vocab_size)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

print('model done')

# Train the model
model.fit(X, y, epochs=50, batch_size=64, validation_split=0.2)

