const hamburger = document.querySelector('#btnHamburger');
const header = document.querySelector('.header');
const overlay = document.querySelector('.overlay');
const fadeElements = document.querySelectorAll('.fade');

btnHamburger.addEventListener('click', function() {
    console.log('open');

    if(header.classList.contains('open')) { // Close hamburger menu
        header.classList.remove('open');
        overlay.classList.remove('fade-in');
        overlay.classList.add('fade-out');
    }
    else { // Open hamburger menu
        header.classList.add('open');
        fadeElements.forEach(function(element) {
            element.classList.remove('fade-out');
            element.classList.add('fade-in');
        });
    }
});
