var fs = require('fs');

// var obj = JSON.parse	(fs.readFileSync('/tmp/', 'utf8'));

exports.getBandwidth = function(request, response) {

	fs.readFile('/tmp/bandwidth.json', (err, data) => {
    	if (err) response.end("Not enough data to populate the bandwidth");
    	let jsonData = JSON.parse(data);
    	response.end(jsonData.all+","+jsonData.service)	
    });		
};