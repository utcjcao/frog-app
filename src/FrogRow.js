import React, { useState } from "react";

let inactiveFrog = "  o  o\n (    )\n/| || |\\n^ ^  ^ ^\n";
let activeFrog = "  o  o\n ([  ])\n/| || |\\n^ ^  ^ ^\n";

const FrogRow = ({ frogStates }) => {
  return (
    <div className="frog-row">
      {frogStates.map((isSinging, index) => (
        <div key={index}>{isSinging ? activeFrog : inactiveFrog}</div>
      ))}
    </div>
  );
};

export default FrogRow;
