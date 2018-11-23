module.exports = function(app) {
 
    var controller = require('../controllers/controller.js');
    var bandWidthController = require('../controllers/bandwidth.js')
 
    //Create a topology
    app.post('/api/createTopology', controller.createTopology);  

    //Get the bandwidth
    app.get('/api/getBandwidth', bandWidthController.getBandwidth);



    // // Create a new Customer
    // app.post('/api/customers', customers.create);
 
    // // Retrieve all Customer
    // app.get('/api/customers', customers.findAll);
 
    // // Retrieve a single Customer by Id
    // app.get('/api/customers/:id', customers.findOne);
 
    // // Update a Customer with Id
    // app.put('/api/customers/:id', customers.update);
 
    // // Delete a Customer with Id
    // app.delete('/api/customers/:id', customers.delete);

    
}