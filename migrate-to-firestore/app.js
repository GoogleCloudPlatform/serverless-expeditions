var express = require('express');
var todocontroller = require('./controllers/todocontroller.js');

var app = express();

// Set up template engine
app.set('view engine', 'ejs');

// Static files
app.use(express.static('./public'));

// Fire controllers
todocontroller(app);

// Listen to port
var listen_port=process.env.PORT || 8080;
app.listen(listen_port);
console.log("Your Listening to the port", listen_port)
