document.addEventListener('DOMContentLoaded', function() { 

    document.querySelectorAll('span.messages-delete').forEach(function(span) {
        span.onclick = function() { deleteMessage(span.dataset.id)} })

})


function deleteMessage(messageid)
        {
         message_row = "message-row-"+messageid

         fetch('deletemessage', { method: 'POST',
                                  body: JSON.stringify({message_id: messageid,})
                                })
         .then(response => { console.log(response.status);
               estado = response.status;
               return response.json() })
         .then(result => {console.log(result);
               if (estado == 201)
                  { document.querySelector('#'+message_row).style.display = 'none';
                  }
                else 
                    { alert(result.message); }
                })
        }