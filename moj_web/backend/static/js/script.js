/* funcionality of slider / Aboutmepage  My_skills */

let isRunning = false;

let slideIndex = 1;

const plusSlides = (n) => {
  showSlides(slideIndex += n);
}

const showSlides = (n) => {
  let i;
  let slides = document.getElementsByClassName("mySlides");
  let dots = document.getElementsByClassName("dot");
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

const makeTrue = (time) => {
  setTimeout( () => {
    isRunning = false;
  }, time);
  setTimeout( () => {
    plusSlides(1)
  }, time);
}


const currentSlide = (n) => {
  showSlides(slideIndex = n);
}

plusSlides(slideIndex)

const automaticSlides = () => {
  setTimeout( () => {
    plusSlides(1)
  }, 5000);
}

automaticSlides()

// UNDERLINE CURRENT PAGE //

// Get the container element
let btnContainer = document.getElementById("nav-link");

// Get all buttons with class="btn" inside the container
let btns = btnContainer.getElementsByClassName("nav-link")[0];

// Loop through the buttons and add the active class to the current/clicked button
for (let i = 0; i < btns.length; i++) {
  btns[i].addEventListener("click", () => {
    let current = document.getElementsByClassName("active");
    current[i].className = current[i].className.replace("active", "");
    this.className += " active";
  });
}
