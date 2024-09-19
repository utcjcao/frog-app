import React, { useEffect, useState } from "react";
import { Midi } from "@tonejs/midi";
import * as Tone from "tone";

const MidiPlayer = ({ midiURL }) => {
  const [midi, setMidi] = useState(null);

  useEffect(() => {
    const loadMidi = async (midiURL) => {
      try {
        // const rawData = await fetch(`/music/${midiURL}`);
        const rawData = await fetch(`/music/example_0.midi`);
        const arrayBuffer = await rawData.arrayBuffer();
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
      if (!midi) return;
      console.log("test");

      // Start Tone.js context
      await Tone.start();

      // Create Tone.js instruments
      const synths = midi.tracks.map(() =>
        new Tone.PolySynth(Tone.Synth, {
          maxPolyphony: 100111111,
        }).toDestination()
      );

      // Schedule notes to be played
      midi.tracks.forEach((track, trackIndex) => {
        track.notes.forEach((note) => {
          synths[trackIndex].triggerAttackRelease(
            note.name,
            note.duration,
            note.time
          );
        });
      });
    }
  };
  return (
    <div>
      <button onClick={playMidi}>Play MIDI</button>
    </div>
  );
};

export default MidiPlayer;
