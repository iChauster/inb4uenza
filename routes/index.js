var express = require('express');
var router = express.Router();
var path = require('path');

/* GET home page. */
router.get('/:strain/:year', function(req, res, next) {
	var strain = req.params.strain;
	var year = req.params.year;
	res.render("./index")
});

module.exports = router;
