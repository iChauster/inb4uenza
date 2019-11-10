var express = require('express');
var Strain = require('../models/strain.js')
var router = express.Router();
var path = require('path');

/* GET home page. */
router.get('/index', function(req, res, next) {
	res.render("index")
});
router.get('/about', function(req, res, next) {
	res.render("about")
});
router.get('/news', function(req, res, next) {
	res.render("news")
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
			avgYear = (parseInt(avgYearArray[0]) + parseInt(avgYearArray[1])) / 2
			yearRange.push(avgYear)

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
			var sendObject = {}
			if (resultH){
				var lastH = (resultH.last) ? true : false
				sendObject["lastH"] = lastH
				sendObject["sequenceH"] = resultH.seq
				sendObject["probabilityIntervalsH"] = resultH.probabilityIntervals
			}
			if (resultN){
				var lastN = (resultN.last) ? true : false
				sendObject["lastN"] = lastN
				sendObject["sequenceN"] = resultN.seq
				sendObject["probabilityIntervalsN"] = resultN.probabilityIntervals
			}
			sendObject["yearRange"] = yearRange
			res.render("index", sendObject)
		}
	})
});

module.exports = router;
