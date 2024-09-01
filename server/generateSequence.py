import numpy as np
import pretty_midi
from tensorflow.keras.models import load_model
import random

def generate_sequence(model, seed_sequence, seq_length, vocab_size, num_generate=100):
    generated_sequence = list(seed_sequence)

    for _ in range(num_generate):
        input_sequence = np.array(generated_sequence[-seq_length:]).reshape(1, seq_length, vocab_size)
        
        predictions = model.predict(input_sequence, verbose=0)
        next_note = np.argmax(predictions[0, -1, :])
        
        generated_sequence.append(next_note)
    
    return generated_sequence

def sequence_to_midi(sequence, output_file):
    midi_data = pretty_midi.PrettyMIDI()
    piano = pretty_midi.Instrument(program=0)

    for i, note_number in enumerate(sequence):
        note = pretty_midi.Note(velocity=100, pitch=note_number, start=i * 0.5, end=(i + 1) * 0.5)
        piano.notes.append(note)
    
    midi_data.instruments.append(piano)
    midi_data.write(output_file)

def generate_random():
    try:
        loaded_model = load_model('../models/test_model.h5')
    except:
        print('loading model error')
    seq_length = 50
    vocab_size = 79  
    sequence = [random.randint(0, 79) for i in range(seq_length)]
    generated_sequence = generate_sequence(loaded_model, sequence, seq_length, vocab_size, num_generate=200)

    return sequence_to_midi(generated_sequence, 'generated_music.mid')

def generate_seeded(sequence):
    try:
        loaded_model = load_model('../models/test_model.h5')
    except:
        print('loading model error')
    seq_length = 50
    vocab_size = 79
    generated_sequence = generate_sequence(loaded_model, sequence, seq_length, vocab_size, num_generate=200)

    return sequence_to_midi(generated_sequence, 'generated_music.mid')