document.addEventListener('DOMContentLoaded', function() {

      fetch('unreadmessages')
             .then(response => response.json())
             .then(data  => {
 
               cantidad= data.unreaded;
 
                if (cantidad > 0) 
                   { document.querySelector('#messages-unreaded').innerHTML = cantidad }
                else
                   { document.querySelector('#messages-unreaded').innerHTML = '' }
           
 
           });          
 
 });

