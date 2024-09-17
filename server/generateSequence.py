import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import pandas as pd
import pretty_midi
from trainModel import mse_with_positive_pressure 

key_order = ['pitch', 'step', 'duration']

def notes_to_midi(
    notes: pd.DataFrame,
    out_file: str, 
    instrument_name: str,
    velocity: int = 100,  # note loudness
    ) -> pretty_midi.PrettyMIDI:

    pm = pretty_midi.PrettyMIDI()
    instrument = pretty_midi.Instrument(
        program=pretty_midi.instrument_name_to_program(
            instrument_name))

    prev_start = 0
    for i, note in notes.iterrows():
        start = float(prev_start + note['step'])
        end = float(start + note['duration'])
        note = pretty_midi.Note(
            velocity=velocity,
            pitch=int(note['pitch']),
            start=start,
            end=end,
        )
        instrument.notes.append(note)
        prev_start = start

    pm.instruments.append(instrument)
    pm.write(out_file)

def predict_next_note(
    notes: np.ndarray, 
    model: tf.keras.Model, 
    temperature: float = 1.0) -> tuple[int, float, float]:
    """Generates a note as a tuple of (pitch, step, duration), using a trained sequence model."""

    assert temperature > 0

    # Add batch dimension
    inputs = tf.expand_dims(notes, 0)

    predictions = model.predict(inputs)
    pitch_logits = predictions['pitch']
    step = predictions['step']
    duration = predictions['duration']

    pitch_logits /= temperature
    pitch = tf.random.categorical(pitch_logits, num_samples=1)
    pitch = tf.squeeze(pitch, axis=-1)
    duration = tf.squeeze(duration, axis=-1)
    step = tf.squeeze(step, axis=-1)

    # `step` and `duration` values should be non-negative
    step = tf.maximum(0, step)
    duration = tf.maximum(0, duration)

    return int(pitch), float(step), float(duration)

def note_to_pitch(note):
    note_map = {
        'C': 0, 
        'D': 2, 
        'E': 4,
        'F': 5, 
        'G': 7, 
        'A': 9, 
        'B': 11
    }
    
    note_name = note[:-1]
    octave = int(note[-1])
    
    pitch = note_map[note_name] + (octave + 1) * 12
    
    return pitch

def sequence_to_notes(sequence):
    start, end = 0, 2
    notes = {
        'pitch': [],
        'start': [],
        'end': [],
        'step': [],
        'duration': []
    }
    for i in range(5):
        for note in sequence:
            notes['pitch'].append(note_to_pitch(note))
            notes['start'].append(start)
            notes['end'].append(end)
            notes['step'].append(2)
            notes['duration'].append(end - start)
            start, end = start + 2, end + 2
    return np.stack([notes[key] for key in key_order], axis=1)



def generate_seeded(sequence, sequence_number, num_predictions=50):
    """
    Generates a midi file based on a seeded sequence

    Parameters:
    sequence (string list): List of characters
    sequence_number (int): id of sequence
    num_predictions (int): number of predicted notes

    Returns:
    generated_midi: midi file of generated music
    """
    seq_length = 25
    vocab_size = 128
    model = load_model('models/test_model.keras', custom_objects={'mse_with_positive_pressure': mse_with_positive_pressure})
    input_notes = (sequence_to_notes(sequence)[:seq_length] / np.array([vocab_size, 1, 1]))
    generated_notes = []
    prev_start = 0
    for _ in range(num_predictions):
        pitch, step, duration = predict_next_note(input_notes, model, temperature=2)
        start = prev_start + step
        end = start + duration
        input_note = (pitch, step, duration)
        generated_notes.append((*input_note, start, end))
        input_notes = np.delete(input_notes, 0, axis=0)
        input_notes = np.append(input_notes, np.expand_dims(input_note, 0), axis=0)
        prev_start = start

    generated_notes = pd.DataFrame(
    generated_notes, columns=(*key_order, 'start', 'end'))
    notes_to_midi(generated_notes, out_file = f'music/example_{sequence_number}.midi', instrument_name="Shakuhachi")