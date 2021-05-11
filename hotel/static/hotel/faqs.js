document.addEventListener('DOMContentLoaded', function() {

    document.querySelectorAll('div.faqs-question').forEach(function(div) {
  
      div.onclick = function() { 

        divChild = this.children[0];

        divChild.classList.toggle("active");

      var panel = this.nextElementSibling;

          if (panel.style.display === "block") 
              {
               panel.style.display = "none";
              } 
          else {
                panel.style.display = "block";
               }
             
            } 
        })
    });