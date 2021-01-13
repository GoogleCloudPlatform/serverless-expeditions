const express = require('express');
const bodyParser = require('body-parser');
const app = express();

app.use(bodyParser.json({ type: '*/*' }));
const port = process.env.PORT || 8080;

app.listen(port, () => {
    console.log('Listening on port', port);
});

app.post('/', (req, res) => {
    const minBalance = parseFloat(req.body.minBalance) || 0;
    console.log(`minBalance: ${minBalance}`);
    billOustandingCustomers(minBalance);
    res.status(204).send();
})

function billOutstandingCustomers(minBalance) { 
    // your business logic here
}