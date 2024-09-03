import React from "react";
import * as Tone from "tone";

const notes = ["C", "D", "E", "F", "G", "A", "B"];

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
    synth.triggerAttackRelease(`${note}${4}`, "8n");
  };

  return (
    <div className="keyboard">
      {notes.map((note, index) => (
        <Key key={index} note={note} onClick={onKeyClick} />
      ))}
    </div>
  );
};

export default Keyboard;
