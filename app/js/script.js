const hamburger = document.querySelector('#btnHamburger');
const header = document.querySelector('.header');
const overlay = document.querySelector('.overlay');
const fadeElements = document.querySelectorAll('.has-fade');

btnHamburger.addEventListener('click', function() {
    console.log('open');

    // Close hamburger menu
    if(header.classList.contains('open')) {
        header.classList.remove('open');
        fadeElements.forEach(function(element) {
            element.classList.remove('fade-in');
            element.classList.add('fade-out');
        });
    }
    // Open hamburger menu
    else { 
        header.classList.add('open');
        fadeElements.forEach(function(element) {
            element.classList.remove('fade-out');
            element.classList.add('fade-in');
        });
    }
});
