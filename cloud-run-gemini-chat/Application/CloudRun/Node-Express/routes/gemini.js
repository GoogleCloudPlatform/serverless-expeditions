var express = require('express');
var router = express.Router();

/* GET gemini page. */
router.get('/', function(req, res, next) {
  res.render('gemini', { title: 'Gemini' });
});

module.exports = router;
