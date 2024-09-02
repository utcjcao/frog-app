import React from "react";
import * as Tone from "tone";

const notes = ["C", "D", "E", "F", "G", "A", "B"];

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

const Keyboard = ({ handleNotePlay }) => {
  const synth = new Tone.Synth().toDestination();

  const onKeyClick = (note) => {
    handleNotePlay(note);
    synth.triggerAttackRelease(`${note}${4}`, "8n");
  };

  return (
    <div className="keyboard">
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
