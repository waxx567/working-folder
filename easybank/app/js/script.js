const hamburger = document.querySelector("#btnHamburger");
const body = document.querySelector("body");
const header = document.querySelector(".header");
const overlay = document.querySelector(".overlay");
const fadeElements = document.querySelectorAll(".has-fade");

btnHamburger.addEventListener("click", function() {
    console.log("hamburger open");

    // Close hamburger menu
    if(header.classList.contains("open")) {
        body.classList.remove("no-scroll");
        header.classList.remove("open");
        fadeElements.forEach(function(element) {
            element.classList.remove("fade-in");
            element.classList.add("fade-out");
        });
    }
    // Open hamburger menu
    else { 
        body.classList.add("no-scroll");
        header.classList.add("open");
        fadeElements.forEach(function(element) {
            element.classList.remove("fade-out");
            element.classList.add("fade-in");
        });
    }
});
