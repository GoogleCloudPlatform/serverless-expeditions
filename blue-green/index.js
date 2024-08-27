const express = require('express');
const app = express();

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log(`App listening on port ${port}`);
});

app.get('/', async (req, res) => {
  const html = `
    <html>
      <body style="background-color: #4D4;">
        <h1>
          Green
        </h1>
      </body>
    </html>
  `;
  res.send(html);
})
