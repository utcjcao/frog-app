import pickle as pkl
import glob
import numpy as np
import pandas as pd
import pretty_midi
import seaborn as sns
import tensorflow as tf
import keras_tuner as kt
from tqdm import tqdm
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout, Activation
from keras import activations
import load_data
import variables
import os

def midi_to_sequence(midi_file):
    midi_data = pretty_midi.PrettyMIDI(midi_file)
    notes = []
    for instrument in midi_data.instruments:
        if not instrument.is_drum:  
            notes.extend([note.pitch for note in instrument.notes])
    return notes

def prepare_sequences(notes, seq_length):
    sequences = []
    for i in range(len(notes) - seq_length):
        seq_in = notes[i:i+seq_length]
        seq_out = notes[i+seq_length]
        sequences.append((seq_in, seq_out))
    return sequences

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
    
    return np.concatenate(processed_X), np.concatenate(processed_y), vocab_size

def build_model(seq_length, vocab_size):
    model = Sequential()
    model.add(Dropout(0.2))
    model.add(LSTM(
        512,
        input_shape=(seq_length, vocab_size),
        return_sequences=True
    ))
    model.add(Dense(256))
    model.add(Dense(256))
    model.add(LSTM(512, return_sequences=True))
    model.add(Dense(256))
    model.add(LSTM(512))
    model.add(Dense(128, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    return model

def create_model():
    load_data.load()
    filenames = glob.glob(str(variables.get_data_dir()/'**/*.mid*'))

    filenames = filenames[:20]
    print('done loading')

    seq_length = 50
    X, y = create_dataset(filenames, seq_length)

    print('done dataset')

    flat_X = [item for sublist in X for item in sublist]  
    flat_y = [item for item in y]  
    all_midi_notes = list(range(128))
    encoder = LabelEncoder()
    encoder.fit(flat_X + flat_y + all_midi_notes)  

    
    batch_size = 1000  
    X, y, vocab_size = preprocess_data_in_batches(X, y, encoder, batch_size)

    print('done preprocess')

    model = build_model(seq_length, vocab_size)

    print('model done')

    model.fit(X, y, epochs=1, batch_size=64, validation_split=0.2)

    file_path = os.path.abspath('models/test_model.keras')

    model.save(file_path) 

if __name__ == '__main__':
    os.makedirs('models', exist_ok=True)
    create_model()


