const express = require('express');
const app = express();
app.use(express.urlencoded({ extended: true }));
const session = require('express-session');
const redis = require('redis');
let RedisStore = require('connect-redis')(session);
const redisClient = require('redis').createClient(
  process.env.REDIS_PORT,
  process.env.REDIS_HOST
);

app.use(session({
  store: new RedisStore({ client: redisClient }),
  secret: 'Q3J9ySAXCV',
  resave: false,
  saveUninitialized: true
}))

const port = process.env.PORT || 8080;
app.listen(port, () => {
  console.log('Listening on port', port);
});

app.get('/', async (req, res) => {
  console.log('get handler')
  console.log('  req.session.cart', req.session.cart);
  let html =
    '<html><body>Shopping cart:' +
    '<p>';
  if (req.session.cart) {
    for (const item of req.session.cart) {
      html += item + '<br>';
    }
  }
  else {
    html += '[Empty cart]';
  }
  html +=
    '</p>' +
    '<form action="/" method="post">' + 
    '<input type="submit" name="command" value="Add a random fruit"/> ' +
    '<input type="submit" name="command" value="Clear cart"/>' +
    '</form>' +
    '</body></html>';
  res.send(html);
})

app.post('/', async (req, res) => {
  console.log('post handler')
  console.log('  req.body', req.body);
  if (req.body.command == 'Add a random fruit') {
    if (!req.session.cart) {
      req.session.cart = [];
    }
    req.session.cart.push(getRandomFruit());
  }
  if (req.body.command == 'Clear cart') {
    req.session.cart = '';
  }
  console.log('  req.session.cart', req.session.cart);
  res.redirect('/');
})

function getRandomFruit() {
  fruits = [
    'Apple', 'Banana', 'Cherries', 'Date Fruit', 'Elderberries', 'Figs',
    'Gooseberries', 'Honeydew Melon', 'Jackfruit', 'Kiwifruit', 'Lemon',
    'Mango', 'Nectarine', 'Orange', 'Papaya', 'Quince', 'Raspberries',
    'Strawberries', 'Tangerine', 'Watermelon'
  ];
  return fruits[Math.floor(Math.random()*fruits.length)];
}