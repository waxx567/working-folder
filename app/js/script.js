const hamburger = document.querySelector("#btnHamburger");

btnHamburger.addEventListener("click", function(){
    console.log("open hamburger");

    if(btnHamburger.classList.contains("extended")) {
        btnHamburger.classList.add("extended");
    }
    else {
        btnHamburger.classList.remove("extended");
    }
});
