import express from "express";
import bodyParser from "body-parser";

const app = express();
const port = 3000;

app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res) => {
  res.render("index.ejs");
});

app.post("/submit", (req, res) => {
  const fName = req.body["fName"];
  const lName = req.body["lName"];
  const letters = fName.length + lName.length;
  console.log(letters);
  res.render("index.ejs", { numOfLetters: letters });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
