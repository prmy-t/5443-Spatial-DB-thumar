const express = require("express");
const cors = require("cors");
const app = express();
const database = require("./dataBase");
app.use(cors());

let num_of_missiles = 0;
app.get("/get-missiles", (req, res) => {
  num_of_missiles = 50;
  database.register_missiles(num_of_missiles, res);
});
app.get("/calculate-hit", (req, res) => {
  database.calculate_hits(num_of_missiles, res);
});

app.listen(8000, () => {
  console.log("listening...");
});
