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

document.querySelector('#booking-check-availability-form').addEventListener('submit', checkavailability);

 
function checkavailability()
                               
    {   // dates to calculate availability

        date_in = document.querySelector('#datein').value;
        date_out = document.querySelector('#dateout').value
        
        // dates to calculate number of nights
        fechaInicio = new Date(document.querySelector('#datein').value).getTime();
        fechaFin = new Date(document.querySelector('#dateout').value).getTime();

        // calculate number of nights
        diff = fechaFin - fechaInicio;
        nights = diff/(1000*60*60*24);
        
        fetch('/availability', { method: 'POST',
                                 body: JSON.stringify({checkindate: date_in,
                                                       checkoutdate: date_out })})
        .then(response => {console.log(response.status);
                           estado = response.status;
                           return response.json()})
        .then(data => {console.log(data);
                       if (estado == 201)
                        {

                        }
                       })
        
        event.preventDefault(); 
               
    }
})