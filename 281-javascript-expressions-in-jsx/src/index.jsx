import React from "react";
import ReactDOM from "react-dom/client";

const root = ReactDOM.createRoot(document.getElementById("root"));

const fname = "stavros";
const lname = "maz";
const num = 4;
root.render(
  <div>
    <h1>hello i am {fname + " " + lname}</h1>
    <p>and my lucky number is {num}</p>
    <p>and this is a random number {Math.floor(Math.random() * 10)}</p>
  </div>,
);

// If you're running this locally in VS Code use the commands:
// npm install
// to install the node modules and
// npm run dev
// to launch your react project in your browser
