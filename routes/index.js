var express = require('express');
var Strain = require('../models/strain.js')
var router = express.Router();
var path = require('path');

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render("index")
});

router.get('/:strain', function(req, res, next) {
	console.log('yo hoe')
	var split = req.params.strain.split("_")
	var strain = split[0]
	var year = split[1]
	console.log(strain)
	console.log(year)
	Strain.findOne({strain: strain, year: year}).then(result => {
		res.render("index", {sequence: result.seq, 
			viewpd: result.last, 
			news: result.news, 
			probabilityIntervals: result.probabilityIntervals,
			strain: result.strain,
			year: result.year})
	}).catch(err => {console.log(err)})
});

module.exports = router;
