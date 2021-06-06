document.addEventListener('DOMContentLoaded', function() { 

   score = 0;

    document.querySelectorAll('button.btn-checkout').forEach(function(button) {
                button.onclick = function() 
                
                     { 
   
                        document.querySelector('#checkout-id').innerHTML = button.dataset.checkout_id;

                        document.querySelector('#checkout-datein').innerHTML = document.querySelector('#datein-'+button.dataset.checkout_id).innerHTML;

                        document.querySelector('#checkout-dateout').innerHTML = document.querySelector('#dateout-'+button.dataset.checkout_id).innerHTML;

                        document.querySelector('#checkout-rooms').innerHTML = document.querySelector('#rooms-'+button.dataset.checkout_id).innerHTML;

                        document.querySelector('#checkout-rooms').innerHTML = document.querySelector('#rooms-'+button.dataset.checkout_id).innerHTML;

                        document.querySelector('#checkout-amount').innerHTML = document.querySelector('#amount-'+button.dataset.checkout_id).innerHTML;

                        document.querySelector('#mybookings-table').style.display = 'none';

                        document.querySelector('#mybookings-checkout-div').style.display = 'block';  
                     
                     } })

    document.querySelectorAll('button.btn-delete').forEach(function(button) {
                button.onclick = function() { deleteBooking(button.dataset.delete_id)} })

    document.querySelectorAll('button.btn-checkin').forEach(function(button) {
                button.onclick = function() { checkinBooking(button.dataset.checkin_id)} })

   document.querySelector('button.btn-cancel').onclick = function() { window.location.href="mybookings" }

   document.querySelector('button.btn-confirm').onclick = function() { checkoutBooking() }

    // get the score by star clicked            
    document.querySelectorAll('input').forEach(function(input) {
                  input.onclick = function() { score = input.value; } })


})


function deleteBooking(booking)
         { 
          fetch('deletebooking', { method: 'POST',
                                   body: JSON.stringify({bookingtodelete: booking})})
          .then(response => { console.log(response.status);

                              if (response.status == 201)
                                 { document.querySelector('#tr-'+booking).style.display = 'none';}
                              else
                                 { window.alert(response.status); }

                              return response.json() })
          .then(result => {console.log(result);
                          alert(result.message)});  
         }


function checkinBooking(booking)
         { 
          fetch('checkinbooking', { method: 'POST',
                                    body: JSON.stringify({bookingtocheckin: booking})})
          .then(response => { console.log(response.status);
                              estado = response.status;
                              return response.json() })
          .then(result => {console.log(result);
                           if (estado == 201)
                           {
                            alert(result.message);
                            location.reload(); } })
         }


function checkoutBooking()
         {
            checkout_booking = document.querySelector('#checkout-id').innerHTML;
            checkout_comment = document.querySelector('#checkout-comment').value;
            checkout_code = (document.querySelector('#checkout-code').value).toUpperCase();
            checkout_score = score;

            if (checkout_code !== 'ABC123')
               { alert("Invalid Code\nCódigo Inválido"); }
            else { alert("hacer fetch")}

            // mandar un fetch con los datos del id de la reserva, el comentario, el código y el score
            // si pudo hacer el checkout oculta la div mybookings-checkout-div y muestra mensaje boostrap
            // si no puede hacer el checkout oculta la div mybookings-checkout-div y muestra mensaje bootstrap
        
         }