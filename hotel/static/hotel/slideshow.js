document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll('img.fotothumbnail').forEach(function(img) {

    img.onclick = function() { openModal();
                               slideIndex = img.dataset.fotoid;
                               showSlides(slideIndex); } });

  document.querySelector('#close-modal').addEventListener('click', () => closeModal());

  document.querySelector('.prev').addEventListener('click', () => {--slideIndex; 
                                                                    if (slideIndex < 1) {slideIndex = 34};
                                                                    showSlides(slideIndex)});

  document.querySelector('.next').addEventListener('click', () => {++slideIndex; showSlides(slideIndex)});

// Open Modal
function openModal() { document.getElementById("myModal").style.display = "block"; }
  
// Close  Modal
function closeModal() { document.getElementById("myModal").style.display = "none"; }

function showSlides(n) {

    var i = 0;

    var slides = document.getElementsByClassName("mySlides");

    if ( n > slides.length ) {slideIndex = 1}

    if ( n < 1 ) {slideIndex = slide.length}

     for (i = 0; i < slides.length; i++) 
         {
          slides[i].style.display = "none";
         } 
 
    // muestro el slideIndex-1 porque el arreglo de slides arranca desde cero    
     
    slides[slideIndex-1].style.display = "block";

  }

});