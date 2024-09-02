import React, { useState, useEffect } from "react";
import SpriteAnimation from "./SpriteAnimation";
import FrogDefaultSheet from "./frog-default.png";
import FrogSingingSheet from "./frog-singing.png";
import "./App.css";
import MidiPlayer from "./MidiPlayer";
import { io } from "socket.io-client";

const App = () => {
  const [frogState, setFrogState] = useState("default");
  const [socket, setSocket] = useState();

  useEffect(() => {
    const s = io("http://localhost:5000");
    setSocket(s);
    socket.emit("initialize");
    return () => {
      s.disconnect();
    };
  }, []);

  function GenerateRandom() {
    setFrogState("default");
  }
  function GenerateSeeded() {
    setFrogState("singing");
  }

  return (
    <div>
      <h1>Ribbit Rhythm</h1>
      {frogState === "default" ? (
        <SpriteAnimation
          spriteSheet={FrogDefaultSheet}
          frameWidth={500}
          frameHeight={500}
          frameCount={4}
          animationSpeed={1000}
        />
      ) : frogState === "singing" ? (
        <SpriteAnimation
          spriteSheet={FrogSingingSheet}
          frameWidth={500}
          frameHeight={500}
          frameCount={5}
          animationSpeed={1000}
        />
      ) : (
        <p> default </p>
      )}

      <div className="button-container">
        <button onClick={GenerateRandom}>Generate random!</button>
        <button onClick={GenerateSeeded}>Make your own!</button>
      </div>
    </div>
  );
};

export default App;
