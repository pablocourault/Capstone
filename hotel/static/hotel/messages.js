document.addEventListener('DOMContentLoaded', function() { 

    document.querySelectorAll('span.messages-delete').forEach(function(span) {
        span.onclick = function() { deleteMessage(span.dataset.id)} })

    document.querySelector('button.messages-btn').onclick = function() { sendMessage() } 
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

function sendMessage()
            {
              message = document.querySelector('#messages-textarea').value;
              
              if (message.length == 0)
                 {
                   alert("Error: empty message.\n\nError: mensaje vacío.\n\nError: mensagem vazia.")
                 }  
              else
                 {
                  fetch('sendmessage', { method: 'POST',
                                          body: JSON.stringify({message_content: message}) })
                  .then(response => { console.log(response.status);
                                      estado = response.status;
                                      return response.json() })
                  .then(result => {console.log(result);
                                   if (estado == 201)
                                      { 
                                        document.querySelector('#messages-textarea').value = '';
                                        location.reload();
                                      }
                                   else 
                                      { alert(result.message); }
                                  })
                 }

            }