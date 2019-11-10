var express = require('express');
var mongoose = require('mongoose');
var app = express();

var Schema = mongoose.Schema;

var strainSchema = new Schema({
	strain: {type: String},
	strainType: {type: String},
	year: {type: String},
	seq: {type: String},
	outbreak: {type: Number},
	last: {type: Boolean},
	probabilityIntervals: [],
	country: {type: String},
	news: [{title: {type: String}, link: {type: String}}]
});

module.exports = mongoose.model("Strain", strainSchema);