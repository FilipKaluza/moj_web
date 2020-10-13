/* funcionality of slider / Aboutmepage  My_skills */

let isRunning = false;

let slideIndex = 1;
plusSlides(slideIndex)

// Next/previous controls
function plusSlides(n) {
  showSlides(slideIndex += n);
}

function automaticSlides() {
  setTimeout(function() {
    plusSlides(1)
  }, 5000);
}

function makeTrue(time) {
  setTimeout(function() {
    isRunning = false;
  }, time);
  setTimeout(function() {
    plusSlides(1)
  }, time);
}


function currentSlide(n) {
  showSlides(slideIndex = n);
}


function showSlides(n) {
  var i;
  var slides = document.getElementsByClassName("mySlides");
  var dots = document.getElementsByClassName("dot");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  for (i = 0; i < dots.length; i++) {
      dots[i].className = dots[i].className.replace("active", "");
  }
  slides[slideIndex-1].style.display = "block";
  dots[slideIndex-1].style.display += "active";
  if(isRunning === false) {
    isRunning = true;
    makeTrue(5000);
  };
  let left = document.getElementsByClassName("perinfo").clientHeight;
}

automaticSlides()

