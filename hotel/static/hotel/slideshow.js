document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll('img.fotothumbnail').forEach(function(img) {

    img.onclick = function() { openModal();
                               showSlides(img.dataset.fotoid); }  });

  document.querySelector('#close-modal').addEventListener('click', () => closeModal());

  document.querySelector('.prev').addEventListener('click', () => plusSlides(-1));

  document.querySelector('.next').addEventListener('click', () => plusSlides(1));


// Open the Modal
function openModal() {
    document.getElementById("myModal").style.display = "block";
  }
  
  // Close the Modal
  function closeModal() {
    document.getElementById("myModal").style.display = "none";
  }
  
  /*
  var slideIndex = 1;

  showSlides(slideIndex);
  */

  //  Next/previous controls
  function plusSlides(n) {
    showSlides(n);
  }
  
  /*
  // Thumbnail image controls
  function currentSlide(n) {
    slideIndex = n;
    showSlides(slideIndex);
  } */
  
  function showSlides(slideIndex) {
    
    var i;

    var slides = document.getElementsByClassName("mySlides");

    if ( slideIndex > 36 ) {slideIndex = 1}
    if ( slideIndex < 1 ) {slideIndex = 36}

     for (i = 1; i < 36; i++) {
      slides[i].style.display = "none";
    } 

    slides[slideIndex].style.display = "block";
  }

});