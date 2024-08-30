import React from "react";
import SpriteAnimation from "./SpriteAnimation";
import spriteSheet from "./frog-sheet.png";
import "./App.css";

const App = () => {
  return (
    <div>
      <h1>Sprite Sheet Animation</h1>
      <SpriteAnimation
        spriteSheet={spriteSheet}
        frameWidth={20}
        frameHeight={20}
        frameCount={5}
        animationSpeed={100}
      />
    </div>
  );
};

export default App;
