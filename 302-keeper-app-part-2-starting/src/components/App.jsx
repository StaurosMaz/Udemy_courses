import React from "react";
import Header from "./Header";
import Footer from "./Footer";
import Note from "./Note";
import notes from "../notes";
function createNotes(notes) {
  return (
    <Note
      key={notes.key}
      id={notes.key}
      title={notes.title}
      content={notes.content}
    />
  );
}
function App() {
  return (
    <div>
      <Header />
      {notes.map(createNotes)}
      <Footer />
    </div>
  );
}

export default App;
