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
	Strain.find({strain: strain, country:"All"}, function(err, documents){
		var r = false
		var resultH;
		var resultN;
		console.log("FOUND " + documents.length)
		documents.forEach((doc) => {
			avgYearArray = doc.year.split("-")
			avgYear = (parseInt(avgYearArray[0]) + parseInt(avgYearArray[1])) / 2
			yearRange.push({strain: doc.strain, year: doc.year, average:parseInt(avgYear)})

			if (doc.year == year){
				r = true
				if (doc.strainType == "H"){
					resultH = doc
				}else{
					resultN = doc
				}
			}
		});
		yearRange.sort(function(a,b){
			return a["average"] - b["average"]
		});

		if (yearRange[0]){
			finalRange = [yearRange[0]["average"]]
		}
		hrefs = []
		for (var i = 1; i < yearRange.length; i ++){
			if(yearRange[i]["average"] - finalRange[finalRange.length-1] >= 2){
				var item = yearRange[i]
				finalRange.push(item["average"])
				hrefs.push("/" + item["strain"] + "_" + item["year"])
			}
		}
		if (finalRange.length > 10){
			finalRange = finalRange.slice(-10)
			hrefs = hrefs.slice(-10)
		}
		console.log(finalRange)
		console.log(hrefs)
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
			sendObject["yearRange"] = finalRange
			sendObject["hrefs"] = hrefs
			res.render("index", sendObject)
		}
	})
});

module.exports = router;
