document.addEventListener('DOMContentLoaded', function() {

  document.querySelectorAll('img.fotothumbnail').forEach(function(img) {

    img.onclick = function() { openModal();
                               slideIndex = img.dataset.fotoid;
                               currentSlide(slideIndex); }  });

  document.querySelector('#close-modal').addEventListener('click', () => closeModal());

  document.querySelector('.prev').addEventListener('click', () => plusSlides(-1));

  document.querySelector('.next').addEventListener('click', () => plusSlides(1));

 // var slideIndex = 1;
// showSlides(slideIndex);

// Open the Modal
function openModal() {
    document.getElementById("myModal").style.display = "block"; }
  
  // Close the Modal
  function closeModal() {
    document.getElementById("myModal").style.display = "none"; }

// Next/previous controls
function plusSlides(x) {
  slideIndex = x + slideIndex;
  alert(slideIndex);
  showSlides(slideIndex);
}
  
// Thumbnail image controls
function currentSlide(n) {
  showSlides(n); }


function showSlides(n) {

    var i = 0;

    var slides = document.getElementsByClassName("mySlides");

    if ( n > slides.length ) {slideIndex = 1}
    if ( n < 1 ) {slideIndex = slide.length}

     for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
    } 

    slides[slideIndex-1].style.display = "block";

  }


});