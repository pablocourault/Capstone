document.addEventListener('DOMContentLoaded', function() {

var today = new Date();
var dd = today.getDate();
var mm = today.getMonth()+1; //January is 0 so need to add 1 to make it 1!
var yyyy = today.getFullYear();

if(dd<10){ dd='0'+dd } 
if(mm<10){ mm='0'+mm } 

today = yyyy+'-'+mm+'-'+dd;
document.getElementById("datein").setAttribute("min", today);

// set date of check-out greater than date of check-in
document.querySelector('#datein').addEventListener('input', () => 
                                { document.getElementById("dateout").setAttribute("min",
                                  document.querySelector('#datein').value ); });

                                  date_in = document.querySelector('#datein').value;
                                  date_out = document.querySelector('#dateout').value;
                                  
                                  // dates to calculate number of nights
                                  fechaInicio = new Date(document.querySelector('#datein').value).getTime();
                                  fechaFin = new Date(document.querySelector('#dateout').value).getTime();
                          
                                  // calculate number of nights
                                  diff = fechaFin - fechaInicio;
                                  var nights = diff/(1000*60*60*24);

                                  if (nights > 0) { document.querySelector('#booking-nights').innerHTML = nights; }

                                  if (nights < 0) { window.alert("check-out date is less than check-in date ")}


// initialize number of rooms booked and amount
var singles_selected = 0;
document.querySelector('#singles_booking').value = singles_selected;
var doubles_selected = 0;
document.querySelector('#doubles_booking').value = doubles_selected;
var triples_selected = 0;
document.querySelector('#triples_booking').value = triples_selected;
var quadruples_selected = 0;
document.querySelector('#quadruples_booking').value = quadruples_selected;
document.querySelector('#amount_booking').value = 0;

// pass values to hidden fields in form named booking-reserve-form
document.querySelector('#datein_booking').value = date_in;
document.querySelector('#dateout_booking').value = date_out;

code = randomString();
document.querySelector('#code_booking').value = code;

user = JSON.parse(document.getElementById('user_id').textContent);
document.querySelector('#user_booking').value = user;


// get the rate by room type
var sr = parseFloat(document.querySelector('#single_rate').innerHTML);
var dr = parseFloat(document.querySelector('#double_rate').innerHTML);
var tr = parseFloat(document.querySelector('#triple_rate').innerHTML);
var qr = parseFloat(document.querySelector('#quadruple_rate').innerHTML);


// listen select and update the total amount and the hidden fields on form named booking-reserve-form
document.querySelector('#singles-select').onchange = function() { singles_selected = this.value; total_amount();
                                                                  document.querySelector('#singles_booking').value = this.value; }


document.querySelector('#doubles-select').onchange = function() { doubles_selected = this.value; total_amount();
                                                                  document.querySelector('#doubles_booking').value = this.value; }

document.querySelector('#triples-select').onchange = function() { triples_selected = this.value; total_amount();
                                                                  document.querySelector('#triples_booking').value = this.value; }

document.querySelector('#quadruples-select').onchange = function() { quadruples_selected = this.value; total_amount(); 
                                                                     document.querySelector('#quadruples_booking').value = this.value; }


// calculate the total amount (number of rooms * rate by type)
function total_amount()
                               
    { total = (((parseInt(singles_selected) * sr) + 
               (parseInt(doubles_selected) * dr) + 
               (parseInt(triples_selected) * tr) + 
               (parseInt(quadruples_selected) * qr)) * nights).toFixed(2);

      document.querySelector('#booking-total').innerHTML = total;
      document.querySelector('#amount_booking').value = total;
     }


// generate random code used when the guest make the ckeckout 
function randomString() {
        var mask = '';
        var chars = 'AAA###'
        if (chars.indexOf('AAA') > -1) mask += 'ABCDEFGHIJKLMNPQRSTUVWXYZ';
        if (chars.indexOf('###') > -1) mask += '0123456789';
        var result = '';
        for (var i = 6; i > 0; --i) result += mask[Math.floor(Math.random() * mask.length)];
        return result;
    }

})