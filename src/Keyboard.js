import React from "react";
import * as Tone from "tone";

const notes = [
  // Natural notes in the 3rd octave
  "C3",
  "D3",
  "E3",
  "F3",
  "G3",
  "A3",
  "B3",

  // Natural notes in the 4th octave (commonly used octave)
  "C4",
  "D4",
  "E4",
  "F4",
  "G4",
  "A4",
  "B4",

  // Natural notes in the 5th octave
  "C5",
  "D5",
  "E5",
  "F5",
  "G5",
  "A5",
  "B5",
];

const Key = ({ onClick, note }) => {
  return (
    <div className={`key`} onClick={() => onClick(note)}>
      {note}
    </div>
  );
};

const Keyboard = ({ handleNotePlay }) => {
  const onKeyClick = (note) => {
    const synth = new Tone.Synth().toDestination();
    handleNotePlay(note);
    synth.triggerAttackRelease(`${note}`, "8n");
  };

  return (
    <div className="keyboard">
      {notes.map((note, index) => (
        <Key key={index} note={note} onClick={onKeyClick} />
      ))}
    </div>
  );
};

// sorry vennise took a break today no useful code :)

export default Keyboard;
