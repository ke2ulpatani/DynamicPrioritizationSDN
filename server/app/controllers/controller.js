var exec = require('child_process').exec;

exports.createTopology = function(request, response) {
	var shellCommand = "sudo python ../python/ssh_to_mininet.py "+request.body.topology+" "+request.body.port_number+" "+ request.body.mac_address+" "+request.body.bandwidth+" &";
    console.log(shellCommand);
    
    exec(shellCommand, function(error, stdout, stderr) {

    console.log('stdout: ' + stdout);
    console.log('stderr: ' + stderr);
    if (error !== null) {
        console.log('exec error: ' + error);
    }
    });

    response.header("Access-Control-Allow-Origin", "*");
    response.header("Access-Control-Allow-Headers", "*");
    response.header("Access-Control-Request-Method", "*");
    response.end();


};