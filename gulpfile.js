// gulp and plugins
var gulp = require('gulp')

// other
var ip = require('quick-local-ip');
var spawn = require('child_process').spawn;

// tasks
gulp.task('start', function() {
    var runserver = spawn(
        'python',
        ['manage.py', 'runserver', ip.getLocalIP4() + ':8000'], 
        { stdio: 'inherit' }
    );
    
    runserver.on('close', function(code) {
        if (code !== 0) {
            console.error('Django runserver exited with error code: ' + code);
        } else {
            console.log('Django runserver exited normally.');
        }
    });
});


