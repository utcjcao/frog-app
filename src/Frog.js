import React, { useState } from "react";

let inactiveFrog = "  o  o\n (    )\n/| || |\\n^ ^  ^ ^\n";
let activeFrog = "  o  o\n ([  ])\n/| || |\\n^ ^  ^ ^\n";

const Frog = ({ isSinging }) => {
  return <div>{isSinging ? activeFrog : inactiveFrog}</div>;
};

export default Frog;
