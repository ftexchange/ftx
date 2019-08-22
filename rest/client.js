//Create a variable for your request type.
let xhr = new XMLHttpRequest;

//Open the connection
xhr.open('GET', 'EXAMPLE:https://cors-anywhere.herokuapp.com/https://ftx.com/api/funding_rates', true);

//Set a request header
xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

//Connect to API
xhr.onload = function() {

//Test API response
if (this.status === 200) {
   var data = (JSON.parse(this.responseText))
   //If the API Responds Call JSON data here
   //Example: var btc = ((data.result[4].rate * 100).toFixed(4) + '%').replace(/"/g);
   
   }}
  
xhr.send();

}
