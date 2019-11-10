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
	Strain.find({strain: strain}, function(err, documents){
		var r = false
		var resultH;
		var resultN;
		console.log("FOUND " + documents.length)
		documents.forEach((doc) => {
			avgYearArray = doc.year.split("-")
			if (doc.year == year){
				r = true
				if (doc.strainType == "H"){
					resultH = doc
				}else{
					resultN = doc
				}
			}
		});

		if (!r){
			console.log('nothin')
		}else{
			last = (result.last) ? result.last : false
			res.render("index", {sequenceN : resultN.seq,
				sequenceH : resultH.seq, 
				viewpd: last, 
				news: result.news, 
				probabilityIntervalsN: resultN.probabilityIntervals,
				probabilityIntervalsH: resultH.probabilityIntervals,
				strain: result.strain,
				year: result.year,
				yearRange: yearRange})
		}
	})
});

module.exports = router;
