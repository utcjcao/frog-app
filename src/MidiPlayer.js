import React, { useEffect } from "react";
import * as Tone from "tone";

const MidiPlayer ({midiURL}) {
    useEffect(() => {
        const loadAndPlayMidi = async () => {
            try {
                const midi = await Tone.Midi.fromUrl(midiURL)

                const synth = new Tone.PolySynth().toDestination()

                midi.tracks.forEach(track => {track.notes.forEach(
                    note => synth.triggerAttackRelease(note.name, note.duration, note.time))})
            } catch (error) {
                console.error("Error loading or playing the MIDI file:", error);
            }
            Tone.Transport.start()
        }
        loadAndPlayMidi();
    }, [midiURL])
}

export default MidiPlayer