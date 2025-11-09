import express from "express";
const app = express();
const port = 3000;
app.get("/", (req, res) => {
  const d = new Date();
  const day = d.getDay();
  let type = "a weekday";
  let adv = "its time to work hard";
  if (day === 0 || day === 6) {
    type = "the weekend";
    adv = "is here";
  }
  res.render("index.ejs", {
    dayType: type,
    advice: adv,
  });
});
app.listen(port, () => {
  console.log(`server is running on port ${port}`);
});
