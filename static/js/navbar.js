function toggleMenuOn() {
    document.querySelector(".navbar").style.backgroundColor = "white";
    document.querySelector(".home").style.display = "none"
    document.querySelector(".toggle-on").style.display = "none"
    document.querySelector(".hide-me").style.display = "block"
    document.querySelector("body").style.maxHeight = "100%"
    document.querySelector(".toggle-off").style.display = "inline"
    document.querySelector("body").style.overflow = "hidden"
    document.querySelector(".navbar-links").style.display = "inline"
}

function toggleMenuOff() {
    const body = document.querySelector("body")
    body.style.maxHeight = "none"
    body.style.overflow = "scroll"
    document.querySelector(".navbar").style.backgroundColor = "hsl(240, 3%, 23%)"
    document.querySelector(".hide-me").style.display = "none"
    document.querySelector(".navbar-links").style.display = "none"
    document.querySelector(".home").style.display = "inline"
    document.querySelector(".toggle-on").style.display = "inline"
    document.querySelector(".toggle-off").style.display = "none"
}
