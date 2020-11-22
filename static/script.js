let navToggle = document.querySelector('.nav');
let alert = document.querySelector('#alert');
let btn = document.querySelector('#btn');
let slideIndex = 1;
let rooms = document.querySelector('#rooms');
let adults1 = document.querySelector('.adults-room1');
let adults2 = document.querySelector('.adults-room2');
let adults3 = document.querySelector('.adults-room3');
let adults4 = document.querySelector('.adults-room4');


showSlides(slideIndex);

btn.addEventListener('click', toggleNav);

// FUNCTIONS

function toggleNav() {
  navToggle.classList.toggle('showNav');
}

function hideAlert() {
  alert.classList.add('hidden');
}

// carousel image
function showSlides(n) {
  if (window.location.href.indexOf("details") > -1) {
    let i;
    let slides = document.querySelectorAll('.mySlides');
    let imgNum = document.querySelectorAll('.imageNumber');

    if (n > slides.length) { slideIndex = 1 }
    if (n < 1) { slideIndex = slides.length }
    for (i = 0; i < slides.length; i++) {
      slides[i].style.display = 'none';
      imgNum[i].style.display = 'none';
    }
    slides[slideIndex - 1].style.display = "block";
    imgNum[slideIndex - 1].style.display = 'block';
  }
}

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

//dynamic rooms options
rooms.onchange = function() {
  let roomsNumber = []
  roomsNumber.length = rooms.value;
  console.log(roomsNumber.length);
  toggleRooms(roomsNumber);
}

function toggleRooms(rooms){
  if (rooms.length === 2) {
    adults2.classList.toggle('hidden');
  } else if (rooms.length === 3) {
    adults2.classList.toggle('hidden');
    adults3.classList.toggle('hidden');
  } else if (rooms.length === 4) {
    adults2.classList.toggle('hidden');
    adults3.classList.toggle('hidden');
    adults4.classList.toggle('hidden');
  }
}




