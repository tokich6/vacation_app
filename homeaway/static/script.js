let navToggle = document.querySelector('.nav');
let alert = document.querySelector('#alert');
let btn = document.querySelector('#btn');
let slideIndex = 1;
let rooms = document.querySelector('#rooms');
let roomsWidget = document.querySelector('.rooms-widget');
let checkIn = document.querySelector('#check-in');
let checkOut = document.querySelector('#check-out');

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
    slides[slideIndex - 1].style.display = 'block';
    imgNum[slideIndex - 1].style.display = 'block';
  }
}

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

// change checkout date based on checkin date selected
if (window.location.pathname == '/') {
  checkIn.onchange = function () {
    let date;
    date = new Date(checkIn.value);
    date.setDate(date.getDate() + 1);
    checkOut.valueAsDate = date
  }
}


//dynamic room options
if (window.location.pathname == '/') {
  rooms.onchange = function () {
    roomsValue = rooms.value;
    let roomCollection = roomsWidget.children;

    for (let i = 0; i < roomCollection.length; i++) {
      if (i + 1 <= roomsValue) {
        roomCollection[i].classList.remove('hidden');
        roomCollection[i].classList.add('selected');
      } else {
        roomCollection[i].classList.remove('selected');
        roomCollection[i].classList.add('hidden');
      }
    }
  }
}





