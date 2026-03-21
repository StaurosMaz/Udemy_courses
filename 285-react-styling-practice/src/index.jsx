//Create a React app from scratch.
//Show a single h1 that says "Good morning" if between midnight and 12PM.
//or "Good Afternoon" if between 12PM and 6PM.
//or "Good evening" if between 6PM and midnight.
//Apply the "heading" style in the styles.css
//Dynamically change the color of the h1 using inline css styles.
//Morning = red, Afternoon = green, Night = blue.
import React from "react";
import ReactDOM from "react-dom/client";

const root = ReactDOM.createRoot(document.getElementById("root"));

const date = new Date();

const time = date.getHours();
let h1Text;
const greetingStyle = {
  color: "",
};
if (time.toString() >= "00" && time.toString() <= "12") {
  h1Text = "good moring";
  greetingStyle.color = "red";
} else if (time.toString() <= "12" && time.toString() >= "18") {
  h1Text = "good good Afternoon";
  greetingStyle.color = "green";
} else {
  h1Text = "good evening";
  greetingStyle.color = "blue";
}

root.render(
  <h1 className="heading" style={greetingStyle}>
    {h1Text}
  </h1>,
);

// If you're running this locally in VS Code use the commands:
// npm install
// to install the node modules and
// npm run dev
// to launch your react project in your browser
