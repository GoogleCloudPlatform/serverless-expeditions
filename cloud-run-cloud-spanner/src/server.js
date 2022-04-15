/**
Express server wrapper script used for running in containers.

See ../index.md for usage info and Apache 2.0 license
*/
/* jslint node: true */
/* jshint esversion: 8 */
'use strict';

const app = require('./app.js');
const Express = require('express');
const bodyParser = require('body-parser');
const express = Express();
const port = process.env.PORT || 443; // Port may be set by runtime environment

express.use(bodyParser.json());

express.get('/', (req, res) => {
  res.status(400).send('Invalid request method');
});

express.get('/user/:username', (req, res) => {
  return app.get_user(req, res);
});

express.get('/users', (req, res) => {
  return app.get_usernames(req, res);
});

express.post('/user', (req, res) => {
  return app.create_user(req, res);
});

express.listen(port, (err) => {
  if (err) {
    return console.log('Express server error', err);
  }

  console.log(`server is listening on ${port}`);
});
