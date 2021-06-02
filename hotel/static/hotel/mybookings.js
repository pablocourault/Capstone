document.addEventListener('DOMContentLoaded', function() { 


document.querySelectorAll('button.btn-checkout').forEach(function(button) {
            button.onclick = function() { alert(button.dataset.checkout_id + ' checkout')} })

document.querySelectorAll('button.btn-delete').forEach(function(button) {
                button.onclick = function() { // alert(button.dataset.delete_id + ' delete')} 
                                              deleteBooking(button.dataset.delete_id)}
                                            })

document.querySelectorAll('button.btn-checkin').forEach(function(button) {
                button.onclick = function() { alert(button.dataset.checkin_id + ' checkin')} })


})

function deleteBooking(booking)
        {

         fetch('deletebooking', { method: 'POST',
                                 body: JSON.stringify({bookingtodelete: booking})})
         .then(response => {console.log(response.status);
                                    estado = response.status;
                                    return response.json()})
         .then(data => { console.log(data);
                        if (estado == 201)
                            {
                             
                            }
                        else
                            { alert("Delete Failed") }
                            })
              
        
        
        }