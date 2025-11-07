import express from "express";
import bodyParser from "body-parser";
import { dirname } from "path";
import { fileURLToPath } from "url";
const app = express();
const port = 3000;
const __dirname = dirname(fileURLToPath(import.meta.url));
app.use(bodyParser.urlencoded({ extended: true }));
var passWord = "";

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/public/index.html");
});
function getPass(req, res, next) {
  passWord = req.body["password"];
  console.log(passWord);
  next();
}
app.use(getPass);

app.post("/check", (req, res) => {
  if (passWord === "010121") {
    res.sendFile(__dirname + "/public/secret.html");
  } else {
    console.log("false password");
  }
});

app.listen(port, () => {
  console.log(`Listening on port ${port}`);
});
