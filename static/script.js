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




