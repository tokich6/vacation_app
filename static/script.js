let navToggle = document.querySelector('#nav');
let alert = document.querySelector('#error-alert');
let slideIndex = 1;
showSlides(slideIndex);

        
function toggleNav() {
  console.log('btn clicked');
  if (!navToggle.classList.contains('hidden')) {
          navToggle.classList.add('hidden');
  } else {
          navToggle.classList.remove('hidden');
  }
}   

let btnToggle = document.querySelector('#btn').addEventListener('click', toggleNav);


function hideAlert () {
   alert.classList.add('hidden');
}

alert.addEventListener('click', hideAlert);

// SLIDESHOW

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}


function showSlides(n) {
  var i;
  var slides = document.querySelectorAll('.mySlides');

  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}


