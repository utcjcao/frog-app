import React, { useState, useEffect } from "react";
import "./App.css";
import * as mm from "@magenta/music";
import FrogRow from "./FrogRow.js";

const App = () => {
  const [modelState, setModelState] = useState("loading");
  const [frogStates, setFrogStates] = useState([false, false, false]);
  const [sequence, setSequence] = useState(null);
  const loadModel = async () => {
    await model.initialize();
    setModelState("finished");
  };
  useEffect(() => {
    loadModel();
  }, []);

  const model = new mm.MusicRNN(
    "https://storage.googleapis.com/magentadata/js/checkpoints/music_rnn/basic_rnn"
  );

  const generateSequence = async () => {
    const seed = {
      notes: [
        { pitch: 60, startTime: 0.0, endTime: 0.5 },
        { pitch: 62, startTime: 0.5, endTime: 1.0 },
        { pitch: 64, startTime: 1.0, endTime: 1.5 },
      ],
      totalTime: 1.5,
    };
    const generatedSequence = await model.continueSequence(seed, 20, 1.0);
    setSequence(generatedSequence);
  };

  const playSequence = async () => {
    if (!sequence) return;
    const player = new mm.SoundFontPlayer(
      "https://storage.googleapis.com/magentadata/js/soundfonts/sgm_plus"
    );
    await player.loadSamples(sequence);
    player.start(sequence);
    sequence.notes.forEach((note, index) => {
      setTimeout(() => {
        const frogIndex = index % frogStates.length;
        triggerFrogAnimation(frogIndex);
      }, note.startTime * 1000);
    });
  };

  const triggerFrogAnimation = (frogIndex) => {
    setFrogStates((prevFrogs) => {
      const newFrogs = [...prevFrogs];
      newFrogs[frogIndex] = true;
      return newFrogs;
    });

    setTimeout(() => {
      setFrogStates((prevFrogs) => {
        const newFrogs = [...prevFrogs];
        newFrogs[frogIndex] = false;
        return newFrogs;
      });
    }, 500);
  };

  return (
    <div>
      <div>
        {modelState == "loading" ? (
          <div>model loading</div>
        ) : (
          <button onClick={generateSequence}>generate !</button>
        )}
      </div>
      <button onClick={playSequence}>play !</button>
      <FrogRow frogs={frogStates} />
    </div>
  );
};

export default App;
