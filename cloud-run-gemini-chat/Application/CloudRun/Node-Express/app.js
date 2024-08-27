var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
const https = require('https');
const session = require('cookie-session')
const { doubleCsrf } = require("csrf-csrf");

const secrets = require('./secrets');
const gemini = require('./gemini');

// Page Routers
var indexRouter = require('./routes/index');
var aboutRouter = require('./routes/about');
var geminiRouter = require('./routes/gemini');

const CSRF_SECRET = "super csrf secret";
const COOKIES_SECRET = "super cookie secret";
const CSRF_COOKIE_NAME = "x-csrf-token";	// This is referenced in app.js

var api_key = null;

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'views'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser(COOKIES_SECRET));
app.use(express.static(path.join(__dirname, 'public')));

// app.use('/', indexRouter);
app.use('/about', aboutRouter);
app.use('/gemini', geminiRouter);

app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: COOKIES_SECRET,
  resave: false,
  saveUninitialized: true,
  cookie: { secure: true }
}))

const { invalidCsrfTokenError, generateToken, doubleCsrfProtection } =
  doubleCsrf({
    getSecret: () => CSRF_SECRET,
    cookieName: CSRF_COOKIE_NAME,
    cookieOptions: { sameSite: false, secure: false, signed: true }, // not ideal for production, development only
  });

// Error handling, validation error interception
const csrfErrorHandler = (error, req, res, next) => {
  if (error == invalidCsrfTokenError) {
    res.status(403).json({
      error: "csrf validation error",
    });
  } else {
    next();
  }
};

// app.use(doubleCsrfProtection);

app.get('/', async (req, res) => {
	const csrfToken = generateToken(req, res);

	res.render('index', {csrfToken: csrfToken});
});

app.post(
	'/ask',
	doubleCsrfProtection,
	csrfErrorHandler,
	async (req, res) => {

	if (!("text" in req.body)) {
		msg = "Error: Form validation failed.";
		res.setHeader('Content-type', 'application/json');
		res.end(create_response(msg));
		return;
	}

	const token = req.body.token;
	const model = req.body.model;
	const question = req.body.text;

	if (question.length == 0) {
		msg = "Please enter a question.";
		res.setHeader('Content-type', 'application/json');
		res.end(create_response(msg));
		return;
	}

	if (api_key == null) {
		api_key = await secrets.init_secrets();
	}

	if (api_key == null) {
		msg = "Error: Secrets Manager access failed";
		res.setHeader('Content-type', 'application/json');
		res.end(create_response(msg));
		return;
	}

	try {
		answer = await gemini.ask_gemini(api_key, model, question);
	} catch (error) {
		console.log(`Exception: ${error.message}`);
		answer = 'Error: request failed. Try again';
	}

	res.setHeader('Content-type', 'application/json');
	res.end(create_response(answer));
})

// catch 404 and forward to error handler
app.use(function(req, res, next) {
  next(createError(404));
});

// error handler
app.use(function(err, req, res, next) {
  // set locals, only providing error in development
  res.locals.message = err.message;
  res.locals.error = req.app.get('env') === 'development' ? err : {};

  // render the error page
  res.status(err.status || 500);
  res.render('error');
});

function create_response(msg) {
  resp = { 'text': msg}
  return JSON.stringify(resp);
}

module.exports = app;
