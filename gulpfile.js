// gulp and plugins
var gulp = require('gulp'),
	run = require('gulp-run');

// other
var ip = require('quick-local-ip');

// rasks
gulp.task('start', function(){
	var local_ip = ip.getLocalIP4();
	var port = ':8000';
	return run('python manage.py runserver ' + local_ip + port).exec()    // prints "Hello World\n". 
    .pipe(gulp.dest('output'))      // writes "Hello World\n" to output/echo. 
  	;
});