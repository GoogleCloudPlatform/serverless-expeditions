const express = require("express");
const app = express();
app.use(express.json());
const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`BarkBark Rest API listening on port ${port}`);
});

app.get("/", async (req, res) => {
  res.json({ status: "Bark bark! Ready to roll!" });
});
