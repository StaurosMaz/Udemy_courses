//Create a react app from scratch.
//It should display a h1 heading.
//It should display an unordered list (bullet points).
//It should contain 3 list elements.
import React from "react";
import ReactDOM from "react-dom/client";
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <>
    <h1 className="heading">Hello i eat</h1>
    <ul>
      <li>egg</li>
      <li>rice</li>
      <li>meat</li>
    </ul>
  </>,
);
// If you're running this locally in VS Code use the commands:
// npm install
// to install the node modules and
// npm run dev
// to launch your react project in your browser
