document.addEventListener('DOMContentLoaded', function() { 

    document.querySelector('button.btn-orders').onclick = function() { makeAnOrder() }

})

function makeAnOrder()
        {
         service_id = document.querySelector('#orders-select').value;
         service_quantity = document.querySelector('#orders-amount').value;

         fetch('makeanorder', { method: 'POST',
                           body: JSON.stringify({service_id: service_id,
                                                 service_quantity: service_quantity })})
         .then(response => { console.log(response.status);
               estado = response.status;
               return response.json() })
         .then(result => {console.log(result);
               if (estado == 201)
                  { document.querySelector('#orders-successful-div').style.display = 'block';
                    document.querySelector('#orders-successful-div').style.animationPlayState = 'running';
                    location.reload();
                      fetch('unreadmessages')
                      .then(response => response.json())
                      .then(data  => {
        
                        cantidad= data.unreaded;
        
                        if (cantidad > 0) 
                            { document.querySelector('#messages-unreaded').innerHTML = cantidad }
                        else
                            { document.querySelector('#messages-unreaded').innerHTML = '' }
                  
        
                      });   
                  }
                else 
                    { alert(result.message); }
                })
        }