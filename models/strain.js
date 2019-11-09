var express = require('express');
var mongoose = require('mongoose');
var app = express();

var Schema = mongoose.Schema;

var strainSchema = new Schema({
	year: {type: Number},
	seq: {type: String},
	news: [{title: {type: String}, link: {type: String}}]
});

module.exports = mongoose.model("Strain", strainSchema);