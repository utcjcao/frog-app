import React, { useEffect, useState } from "react";
import { Midi } from "@tonejs/midi";
import * as Tone from "tone";

const MidiPlayer = ({ notes }) => {
  const playMidi = async () => {
    await Tone.start();
    const synth = new Tone.Synth().toDestination();
    notes.forEach((note) => {
      const { pitch, start, duration } = note;
      synth.triggerAttackRelease(
        Tone.Frequency(pitch, "midi").toFrequency(), // Convert MIDI pitch to frequency
        duration,
        Tone.Transport.now() + start // Schedule start time in Tone.js Transport
      );
    });

    // Start the transport
    Tone.Transport.start();
  };
  return (
    <div>
      <button onClick={playMidi}>Play MIDI</button>
    </div>
  );
};

export default MidiPlayer;
