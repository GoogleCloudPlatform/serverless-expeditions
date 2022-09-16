/**
Main applicaiton script for user microservice. Called by server.js.

See ../index.md for usage info and Apache 2.0 license
*/
/* jslint node: true */
/* jshint esversion: 8 */
'use strict';

/* Cloud run variables */
const DEBUG_LOGGING = process.env.USER_DEBUG || false;
const VERSION_LOGGING = process.env.USER_VERSION_LOGGING || true;

const { v4: uuidv4 } = require('uuid');

// This log line is helpful to keep track of which version of the tokenizer is running.
const appVersion = require('fs').statSync(__filename).mtimeMs + ' env:' + process.env.NODE_ENV;
logVersion(`Users Backend LAUNCHED v.${appVersion}`);


// Cloud Spanner setup
const {Spanner} = require('@google-cloud/spanner');
const spanner = new Spanner();

const SESSION = {
    // If set to true, an error will be thrown when there are no available sessions for a request.
    fail: false,
    // Maximum number of resources to create at any given time.
    max: 20,
    // Maximum number of idle resources to keep in the pool at any given time.
    maxIdle: 10,
    // Minimum number of resources to keep in the pool at any given time.
    min: 1,
};

// Gets a reference to a Spanner instance and database
const instance = spanner.instance("users-staging");
const database = instance.database("users_spanner", SESSION);

/**
 * Endpoint to create user.
 *
 * @param {Object} req create user request context.
 * @param {Object} res create user response context.
 */
exports.create_user = async (req, res) => {
  const usersTable = database.table("users");
  const emailRegexp = /^[-!#$%&'*+\/0-9=?A-Z^_a-z{|}~](\.?[-!#$%&'*+\/0-9=?A-Z^_a-z`{|}~])*@[a-zA-Z0-9](-*\.?[a-zA-Z0-9])*\.[a-zA-Z](-?[a-zA-Z0-9])+$/;

  var reqUsername = String(req.body.username);
  var reqEmail = String(req.body.email);

  if (!reqUsername) {
    debug('Username: '+reqUsername);
    return res.status(500).send('Invalid input for username');
  }

  if (!reqEmail || !emailRegexp.test(reqEmail)) {
    debug('Email: '+reqEmail);
    return res.status(500).send('Invalid input for email');
  }

  // Execute the query
  try {
    const uuid=uuidv4();

    // Create user object
    const user = {
        id: uuid,
        username: reqUsername,
        email: reqEmail,
        created: Spanner.timestamp(new Date())
    }

    // GenerateUser is insert-only. This is done with mutations, not transactions.
    await usersTable.insert([user]);

    res.write(uuid);
    res.status(200).end();
  } catch (err) {
    debug(err)
    res.status(500).send(`Error generating user: ${err}`);
  }
};

/**
 * Endpoint to get user by username.
 *
 * @param {Object} req get user request context.
 * @param {Object} res get user response context.
 */
 exports.get_user = async (req, res) => {
  var reqUsername = String(req.params.username);

  if (!reqUsername) {
    debug('Username: '+reqUsername);
    return res.status(500).send('Invalid input for username');
  }

  try {
    const query = {
      sql: `SELECT * FROM users WHERE username = @username`,
      params: {
        username: reqUsername,
      },
    };

    const [userRow] = await database.run(query);

    if (userRow.length != 1) {
      throw new Error("No matches for the user");
    }
    userRow.forEach(user => {
      res.json(user.toJSON());
    })

    res.status(200).end();
  } catch (err) {
    debug(err)
    res.status(500).send(`Error retrieving user: ${err}`);
  }
 }

/**
 * Endpoint to list of usernames.
 * This is a testing function to retrieve a list of usernames for load testing
 *
 * @param {Object} req get usernames request context.
 * @param {Object} res get usernames response context.
 */
exports.get_usernames = async (req, res) => {
  try {
    const query = {
      sql: `SELECT username FROM users ORDER BY created DESC LIMIT 1000`
    };

    const [userRow] = await database.run(query);

    res.write(JSON.stringify(userRow))

    res.status(200).end();
  } catch (err) {
    debug(err)
    res.status(500).send(`Error retrieving user: ${err}`);
  }
}

/**
 * Endpoint to retrieve a random user.
 * This is a temporary function to handle reading a random user for load testing purposes.
 *
 * @param {Object} req get user request context.
 * @param {Object} res get user response context.
 */
 exports.get_random_user = async (req, res) => {
  var reqOffset = parseInt(req.params.userID);

  if (!reqOffset || reqOffset < 0) {
    debug('Offset: '+reqOffset);
    return res.status(500).send('Invalid input for offset');
  }

  try {
    const query = {
      sql: `SELECT * FROM users ORDER BY created DESC LIMIT 1 OFFSET ${reqOffset}`
    };

    const [userRow] = await database.run(query);

    if (userRow.length != 1) {
      throw new Error("No matches for the user");
    }
    userRow.forEach(user => {
      res.json(user.toJSON());
    })

    res.status(200).end();
  } catch (err) {
    debug(err)
    res.status(500).send(`Error retrieving user: ${err}`);
  }
};


/**
 * Helpful debug function that checks for the var DEBUG_LOGGING == true before writing to console.log()
 */
 function debug (...args) {
  if (DEBUG_LOGGING) console.log(...args);
}

/**
 * A handy utility function that can write the timestamp of app.js when the tokenizer
 * is first launched and again each time it is executed. This is helpful when trying
 * to link log output of a particular run to the code version that generated it.
 */
function logVersion (...args) {
  if (VERSION_LOGGING) console.log(...args);
}
