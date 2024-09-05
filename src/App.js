import React, { useState, useEffect } from "react";
import SpriteAnimation from "./SpriteAnimation";
import FrogDefaultSheet from "./sprite-sheets/frog-default.png";
import FrogSingingSheet from "./sprite-sheets/frog-singing.png";
import "./App.css";
import MidiPlayer from "./MidiPlayer";
import Keyboard from "./Keyboard";
import { io } from "socket.io-client";
import GenerateSeeded from "./GenerateSeeded";

const App = () => {
  const [socket, setSocket] = useState();
  const [recordedNotes, setRecordedNotes] = useState([]);

  useEffect(() => {
    const s = io("http://localhost:5000");
    setSocket(s);
    return () => {
      s.disconnect();
    };
  }, []);

  const handleNotePlay = (note) => {
    if (socket == null) return;
    setRecordedNotes((prevNotes) => [...prevNotes, note]);
    if (recordedNotes.length === 5) {
      socket.emit("generate-sequence", recordedNotes);
      setRecordedNotes([note]);
    }
  };
  useEffect(() => {
    if (socket == null) return;
    const handler = (sequence_number) => {
      let filepath = `../server/music/example_${sequence_number}.midi`;
      MidiPlayer(filepath);
    };
    socket.on("recieve-sequence", handler);
    return () => {
      socket.off("recieve-sequence", handler);
    };
  }, [socket]);

  return (
    <div>
      <Keyboard handleNotePlay={handleNotePlay}></Keyboard>
      <p>{recordedNotes}</p>
    </div>
  );
};

export default App;
