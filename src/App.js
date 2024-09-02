import React, { useState, useEffect } from "react";
import SpriteAnimation from "./SpriteAnimation";
import FrogDefaultSheet from "./frog-default.png";
import FrogSingingSheet from "./frog-singing.png";
import "./App.css";
import MidiPlayer from "./MidiPlayer";
import Keyboard from "./Keyboard";
import { io } from "socket.io-client";
import GenerateSeeded from "./GenerateSeeded";

const App = () => {
  const [frogState, setFrogState] = useState("default");
  const [socket, setSocket] = useState();
  const [recordedNotes, setRecordedNotes] = useState([]);

  const handleNotePlay = (note) => {
    setRecordedNotes((prevNotes) => [...prevNotes, note]);
    if (recordedNotes.length === 5) {
      socket.emit("generate-sequence", recordedNotes);
      setRecordedNotes([note]);
    }
  };
  useEffect(() => {
    const handler = (sequence) => {
      MidiPlayer(sequence);
    };
    socket.on("recieve-sequence");
  }, [socket]);
  useEffect(() => {
    const s = io("http://localhost:5000");
    setSocket(s);
    s.emit("initialize");
    return () => {
      s.disconnect();
    };
  }, []);

  return (
    <div>
      <Keyboard handleNotePlay={handleNotePlay}></Keyboard>
      <p>{recordedNotes}</p>
    </div>
  );
};

export default App;
