import numpy as np
import pretty_midi
from tensorflow.keras.models import load_model
import numpy as np
from tensorflow.keras.utils import to_categorical

def notes_to_midi(notes):
    note_to_midi = {
        'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71,
        'C2': 72, 'D2': 74, 'E2': 76, 'F2': 77, 'G2': 79, 'A2': 81, 'B2': 83
    }

    midi_notes = [note_to_midi[note] for note in notes if note in note_to_midi]
    return midi_notes

def generate_sequence(model, seed_sequence, seq_length, vocab_size, num_generate=100):
    generated_sequence = list(seed_sequence)

    for _ in range(num_generate):
        input_sequence = np.array(generated_sequence[-seq_length:]).reshape(1, seq_length, vocab_size)
        
        predictions = model.predict(input_sequence, verbose=0)
        print(predictions.shape)
        next_note = np.argmax(predictions[0])
        
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
    vocab_size = 128
    print(sequence)
    print(notes_to_midi(sequence))
    seeded_sequence = notes_to_midi(sequence) * 10
    encoded_notes = to_categorical(seeded_sequence, num_classes=vocab_size)
    input_sequence = encoded_notes.reshape(1, seq_length, vocab_size)
    
    generated_sequence = generate_sequence(loaded_model, input_sequence, seq_length, vocab_size, num_generate=200)

    return sequence_to_midi(generated_sequence, 'generated_music.mid')