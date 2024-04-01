const express = require('express');
const app = express();
const cors = require('cors');
const bodyParser = require('body-parser');

const port = 3000;

app.use(cors());
app.use(bodyParser.json());

app.listen(port, () => {
  console.log(`Example app listening on port ${port}`)
})

const matrixDiag = require('./exercises/001-MatrixDiagonalization/matrixDiag.js');

app.post('/exercises/matrix-diagonalization', async function(req, res) {
  let result;
  try {
    console.log("received request : " + req);
    result = await matrixDiag(req.body);
    res.status(200);
  } catch (error) {
    console.log(error);
    res.status(400);
  }
  console.log(result);
  res.send(result);
});

