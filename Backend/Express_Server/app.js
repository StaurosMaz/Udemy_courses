import express from "express";
const app = express();
app.get("/", (req, res) => {
  res.send("hello World");
});
app.get("/contact", (req, res) => {
  res.send("hello contact");
});
app.get("/about", (req, res) => {
  res.send("hello about");
});

app.listen(3000, () => {
  console.log("server running on port 3000.");
});
