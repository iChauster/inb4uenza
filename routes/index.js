var express = require('express');
var Strain = require('../models/strain.js')
var router = express.Router();
var path = require('path');

/* GET home page. */
router.get('/', function(req, res, next) {
	res.render("about")
});

router.get('/:strain', function(req, res, next) {
	console.log('yo hoe')
	var split = req.params.strain.split("_")
	var strain = split[0]
	var year = split[1]

	yearRange = []
	console.log(strain)
	Strain.find({strain: strain}, function(err, documents){
		var r = false
		var result;
		console.log("FOUND " + documents.length)
		documents.forEach((doc) => {
			yearRange.push(doc.year)
			if (doc.year == year){
				r = true
				result = doc
			}
		});

		if (!r){
			console.log('nothin')
		}else{
			last = (result.last) ? result.last : false
			res.render("index", {sequence: result.seq, 
				viewpd: last, 
				news: result.news, 
				probabilityIntervals: result.probabilityIntervals,
				strain: result.strain,
				year: result.year,
				yearRange: yearRange})
		}
	})
	
});

module.exports = router;
