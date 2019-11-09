var createError = require('http-errors');
var express = require('express');
var path = require('path');
var cookieParser = require('cookie-parser');
var logger = require('morgan');
var mongoose = require('mongoose');
var parse = require('csv-parse');
var fs = require('fs');
var Strain = require('./models/strain')

var indexRouter = require('./routes/index');
var usersRouter = require('./routes/users');

var app = express();

// view engine setup
app.set('views', path.join(__dirname, 'routes'));
app.set('view engine', 'ejs');

app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));

app.use('/', indexRouter);
app.use('/users', usersRouter);

mongoose.connect(process.env.MLAB_URI || "mongodb://savan:isrobot1@ds241278.mlab.com:41278/hackpton2019", function (err) {
	if(err) console.log(err);
});
var db = mongoose.connection;
db.on('error', console.error.bind(console, 'connection error:'));
db.once('open', (callback) => {
	console.log('connection succ');
});

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

app.listen(1000);

function addStrain() {
	var pathName = "";
	fs.createReadStream(pathName)
	    .pipe(parse({delimiter: ','}))
	    .on('data', function(csvrow) {
	        console.log(csvrow);
	    })
	    .on('end',function() {
	      //do something wiht csvData
	      console.log(csvData);
	    });
}

module.exports = app;
