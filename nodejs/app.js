var express = require('express');
let winston = require('winston');

let logger = winston.createLogger({
	level:'info',
	format:winston.format.combine(
		winston.format.timestamp(),
		winston.format.printf(info => {
			return `${info.timestamp} ${info.level}: ${info.message}`;
		})
	),
	transports: [new winston.transports.Console()]
	//transports: [new winston.transport.Console()]
});

logger.info("test");
	
var app = express();
var routes = require('./routes');
var path = require('path');

app.set('view engine','ejs');
app.use(express.static(path.join(__dirname,'public')));
app.set('views', path.join(__dirname, 'views'));

app.get('/starwars/', routes.home);
/*app.get('/starwars/',function(req,res){
	res.send("home");
});*/

/*app.get('/starwars/star_wars_episode/',function(req,res){
	res.send("episode");
});*/
app.get('/starwars/star_wars_episode/:episode_number?', routes.movie_single);
app.get('/starwars/*', routes.notFound);

//app.listen(process.env.PORT || 6061);
const port = process.env.PORT || 6061;
app.listen(port, () => {console.log(`App is listening on http://127.0.0.1:${port}`)});
