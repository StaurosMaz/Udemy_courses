import React, { useState } from "react";

function App() {
  const [headingText, setHeadingText] = useState("hello");
  const [headingStyle, setHeadingStyle] = useState(false);
  function handleClick() {
    setHeadingText("all good");
  }

  function mouseOverHandle() {
    setHeadingStyle(true);
    console.log("true");
  }
  function mouseOutHandle() {
    setHeadingStyle(false);
    console.log("fasle");
  }

  return (
    <div className="container">
      <h1>{headingText}</h1>
      <input type="text" placeholder="What's your name?" />
      <button
        style={{ backgroundColor: headingStyle ? "black" : "white" }}
        onMouseOver={mouseOverHandle}
        onMouseOut={mouseOutHandle}
        onClick={handleClick}
      >
        Submit
      </button>
    </div>
  );
}

export default App;
