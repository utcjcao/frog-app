import numpy as np
import pretty_midi
from tensorflow.keras.models import load_model
import random

def notes_to_midi(notes):
    note_to_midi = {
        'C': 60, 'C#': 61, 'D': 62, 'D#': 63, 'E': 64, 'F': 65, 'F#': 66, 'G': 67, 'G#': 68, 'A': 69, 'A#': 70, 'B': 71,
        'C2': 72, 'C#2': 73, 'D2': 74, 'D#2': 75, 'E2': 76, 'F2': 77, 'F#2': 78, 'G2': 79, 'G#2': 80, 'A2': 81, 'A#2': 82, 'B2': 83
    }

    midi_notes = [note_to_midi[note] for note in notes if note in note_to_midi]
    return midi_notes

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

def generate_seeded(sequence):
    try:
        loaded_model = load_model('models/test_model.keras')
    except:
        print('loading model error')
    seq_length = 50
    vocab_size = 44
    seeded_sequence = notes_to_midi(sequence) * 5
    generated_sequence = generate_sequence(loaded_model, seeded_sequence, seq_length, vocab_size, num_generate=200)

    return sequence_to_midi(generated_sequence, 'generated_music.mid')