let navToggle = document.querySelector('#nav');
let alert = document.querySelector('#error-alert');

        
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


function nextSlide(){
        let activeSlide = document.querySelector('.active');
        console.log(activeSlide)
        activeSlide.classList.remove('active');
        activeSlide.classList.add('inactive');
        
        let nextSlide = activeSlide.nextElementSibling;
        console.log(nextSlide)
        nextSlide.classList.remove('inactive');
        nextSlide.classList.add('active');
    }
    
    function previousSlide(){
        let activeSlide = document.querySelector('.active');
        console.log(activeSlide)
        activeSlide.classList.remove('active');
        activeSlide.classList.add('inactive');
        
        let previousSlide = activeSlide.previousElementSibling;
        console.log(previousSlide)
        previousSlide.classList.remove('inactive');
        previousSlide.classList.add('active');
    }




