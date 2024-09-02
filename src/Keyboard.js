import React from "react";
import * as Tone from "tone";

const notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"];

const Key = ({ isSharp, onClick, note }) => {
  return (
    <div
      className={`key ${isSharp ? "sharp" : "natural"}`}
      onClick={() => onClick(note)}
    >
      {note}
    </div>
  );
};

const Keyboard = () => {
  const synth = new Tone.Synth().toDestination();

  const onKeyClick = (note) => {
    const octave = 4;
    synth.triggerAttackRelease(`${note}${octave}`, "8n");
  };

  return (
    <div className="Keyboard">
      {notes.map((note, index) => (
        <Key
          key={index}
          note={note}
          onClick={onKeyClick}
          isSharp={note.includes("#")}
        />
      ))}
    </div>
  );
};

export default Keyboard;
