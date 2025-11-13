import express from "express";
import bodyParser from "body-parser";
const app = express();

app.set("view engine", "ejs");
const posts=[]
app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

app.get("/", (req, res) => {
  res.render("home", { posts: posts });
});

app.get("/compose", (req, res) => {
  res.render("compose");
});

app.post("/compose", (req, res) => {
  const post = {
    title: req.body.postTitle,
    content: req.body.postBody
  };
  posts.push(post);
  res.redirect("/");
});

app.get("/posts/:postTitle", (req, res) => {
  const requestedTitle = req.params.postTitle.toLowerCase();

  posts.forEach(post => {
    if (post.title.toLowerCase() === requestedTitle) {
      res.render("post", { title: post.title, content: post.content });
    }
  });
});


app.listen(3000, () => {
  console.log("Server started on port 3000");
});
