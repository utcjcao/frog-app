import React, { useEffect, useState } from "react";
import { Midi } from "@tonejs/midi";
import * as Tone from "tone";

const MidiPlayer = ({ midiURL }) => {
  const [midi, setMidi] = useState(null);

  useEffect(() => {
    const loadMidi = async () => {
      try {
        const response = await fetch(midiURL);
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const arrayBuffer = await response.arrayBuffer();
        const midiData = new Midi(arrayBuffer);
        setMidi(midiData);
      } catch (error) {
        console.error("Error loading MIDI file:", error);
      }
    };
    loadMidi();
  }, [midiURL]);

  const playMidi = async () => {
    if (midi) {
      const synth = new Tone.Synth().toDestination();

      midi.tracks.forEach((track) => {
        track.notes.forEach((note) => {
          synth.triggerAttackRelease(
            note.name,
            note.duration,
            note.time,
            note.velocity
          );
        });
      });

      Tone.Transport.start();
    }
  };
  return (
    <div>
      <button onClick={playMidi}>Play MIDI</button>
    </div>
  );
};

export default MidiPlayer;
