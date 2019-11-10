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

  // render the erfdror page
  res.status(err.status || 500);
  res.render('error');
});

app.listen(1005);

function addStrain(strainName, pathToFile) {
	var pathName = pathToFile;
	var strain;
	var documentsToSave = []
	fs.createReadStream(pathName)
	    .pipe(parse({delimiter: ','}))
	    .on('data', function(csvrow) {
	        strain = new Strain()
	        firstColumn = csvrow.shift()
	        
	        var yearRange = csvrow.shift()
	        if (yearRange == "year_range")
	        	return	        
	        var probIntervals = JSON.parse(csvrow.shift())
	        console.log(probIntervals.length)
	        var sequence = csvrow.shift()

	        strain.strain = strainName
	        strain.year = yearRange
	        strain.seq = sequence
	        strain.probabilityIntervals = probIntervals

	        documentsToSave.push(strain)

	    })
	    .on('end',function() {
	    	console.log("LAST STRAIN")
	    	console.log(strain)
	    	strain.last = true;
	    	
	    	for (var s in documentsToSave) {
	    		console.log(documentsToSave[s].last)
	    		documentsToSave[s].save();
	    	}
	      //do something wiht csvData
	    })
	    .on('error', function(err){
	    	console.log(err);
	    })
}

function getSeverity(strain){
	var maxH = 3
	var maxN = 7

	for (var h = 1; h <= maxH; h ++){
		
	}

}
function getRecent(strain, strainType){
	Strain.findOne({strain: strain, last: true, strainType: strainType}).then(result => {
		var array = result.probabilityIntervals;
		array.sort(function(a,b){
			return b[1] - a[1]
		});
		return array.slice(0,3)
	}).catch(err => {console.log(err)})
}

getRecent("H3N2");
//addStrain("H3N2", "H3N2_4_China")

module.exports = app;
