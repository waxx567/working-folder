const btnHamburger = document.querySelector('#btnHamburger');
const body = document.querySelector('body');
const header = document.querySelector('.header');
const overlay = document.querySelector('.overlay');
const faders = document.querySelectorAll('.has-fade');

btnHamburger.addEventListener('click', function(){
    console.log('click hamburger');

    // Close hamburger menu
    if(header.classList.contains('open')) {
        body.classList.remove('noscroll');
        header.classList.remove('open');
        faders.forEach(function (item) {
            item.classList.remove('fade-in');
            item.classList.add('fade-out');
        });
    }
    // Open hamburger menu
    else {
        body.classList.add('noscroll');
        header.classList.add('open');
        faders.forEach(function (item) {
            item.classList.remove('fade-out');
            item.classList.add('fade-in');
        });
    }
});
 