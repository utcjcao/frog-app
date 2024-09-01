import React, { useState, useEffect } from "react";

const arr = [0, 1, 2, 3, 4, 3, 2, 1];

const SpriteAnimation = ({
  spriteSheet,
  frameWidth,
  frameHeight,
  frameCount,
  animationSpeed,
}) => {
  const [currentFrameIndex, setCurrentFrameIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentFrameIndex(
        (prevFrameIndex) => (prevFrameIndex + 1) % arr.length
      );
    }, animationSpeed);

    return () => clearInterval(interval);
  }, [frameCount, animationSpeed]);

  return (
    <div
      style={{
        width: `${frameWidth}px`,
        height: `${frameHeight}px`,
        backgroundImage: `url(${spriteSheet})`,
        backgroundPosition: `-${arr[currentFrameIndex] * frameWidth}px 0px`,
        backgroundRepeat: "no-repeat",
      }}
    ></div>
  );
};

export default SpriteAnimation;
