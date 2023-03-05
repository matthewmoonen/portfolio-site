


window.onresize = fixDisplayMobileDesktop;
window.onload = fixDisplayMobileDesktop;
function fixDisplayMobileDesktop() {
    if($(window).width() > 991){
    // Stop navbar text/icons disappearing on window resize
    document.querySelector(".navbar-links").style.display = "inline";
    addHoverListeners()
} else {
        removeHoverListeners()
        toggleMenuOff()
        // Remove hover event listeners
}
}



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

function removeHoverListeners() {
    // document.querySelector("#text-links").style.color= "black;"
    document.querySelector("#text-link0").removeEventListener("mouseover", mouseOver0);
    document.querySelector("#text-link0").removeEventListener("mouseout", mouseOut0);
    document.querySelector("#text-link1").removeEventListener("mouseover", mouseOver1);
    document.querySelector("#text-link1").removeEventListener("mouseout", mouseOut1);
    document.querySelector("#text-link2").removeEventListener("mouseover", mouseOver2);
    document.querySelector("#text-link2").removeEventListener("mouseout", mouseOut2);
    document.querySelector("#icon-link0").removeEventListener("mouseover", mouseOver00);
    document.querySelector("#icon-link0").removeEventListener("mouseout", mouseOut00);
    document.querySelector("#icon-link1").removeEventListener("mouseover", mouseOver01);
    document.querySelector("#icon-link1").removeEventListener("mouseout", mouseOut01);
    document.querySelector("#icon-link2").removeEventListener("mouseover", mouseOver02);
    document.querySelector("#icon-link2").removeEventListener("mouseout", mouseOut02);
}

function addHoverListeners() {
    document.querySelector("#text-link0").addEventListener("mouseover", mouseOver0);
    document.querySelector("#text-link0").addEventListener("mouseout", mouseOut0);
    document.querySelector("#text-link0").addEventListener("mouseover", mouseOver0);
    document.querySelector("#text-link0").addEventListener("mouseout", mouseOut0);
    document.querySelector("#text-link1").addEventListener("mouseover", mouseOver1);
    document.querySelector("#text-link1").addEventListener("mouseout", mouseOut1);
    document.querySelector("#text-link2").addEventListener("mouseover", mouseOver2);
    document.querySelector("#text-link2").addEventListener("mouseout", mouseOut2);
    document.querySelector("#icon-link0").addEventListener("mouseover", mouseOver00);
    document.querySelector("#icon-link0").addEventListener("mouseout", mouseOut00);
    document.querySelector("#icon-link1").addEventListener("mouseover", mouseOver01);
    document.querySelector("#icon-link1").addEventListener("mouseout", mouseOut01);
    document.querySelector("#icon-link2").addEventListener("mouseover", mouseOver02);
    document.querySelector("#icon-link2").addEventListener("mouseout", mouseOut02);
}

function mouseOver0() {
    document.querySelector("#text-link1").style.color = "var(--hoverColour)";
    document.querySelector("#text-link2").style.color = "var(--hoverColour)";
    document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
    document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
    document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
}
function mouseOut0() {
    document.querySelector("#text-link1").style.color = "var(--mainColour)";
    document.querySelector("#text-link2").style.color = "var(--mainColour)";
    document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
    document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
    document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
}
function mouseOver1() {
    document.querySelector("#text-link0").style.color = "var(--hoverColour)";
    document.querySelector("#text-link2").style.color = "var(--hoverColour)";
    document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
    document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
    document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
}
function mouseOut1() {
    document.querySelector("#text-link0").style.color = "var(--mainColour)";
    document.querySelector("#text-link2").style.color = "var(--mainColour)";
    document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
    document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
    document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
}
function mouseOver2() {
    document.querySelector("#text-link0").style.color = "var(--hoverColour)";
    document.querySelector("#text-link1").style.color = "var(--hoverColour)";
    document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
    document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
    document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
}
function mouseOut2() {
    document.querySelector("#text-link0").style.color = "var(--mainColour)";
    document.querySelector("#text-link1").style.color = "var(--mainColour)";
    document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
    document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
    document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
}
function mouseOver00() {
    document.querySelector("#text-link0").style.color = "var(--hoverColour)";
    document.querySelector("#text-link1").style.color = "var(--hoverColour)";
    document.querySelector("#text-link2").style.color = "var(--hoverColour)";
    document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
    document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
}
function mouseOut00() {
    document.querySelector("#text-link0").style.color = "var(--mainColour)";
    document.querySelector("#text-link1").style.color = "var(--mainColour)";
    document.querySelector("#text-link2").style.color = "var(--mainColour)";
    document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
    document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
}

function mouseOver01() {
    document.querySelector("#text-link0").style.color = "var(--hoverColour)";
    document.querySelector("#text-link1").style.color = "var(--hoverColour)";
    document.querySelector("#text-link2").style.color = "var(--hoverColour)";
    document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
    document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
}
function mouseOut01() {
    document.querySelector("#text-link0").style.color = "var(--mainColour)";
    document.querySelector("#text-link1").style.color = "var(--mainColour)";
    document.querySelector("#text-link2").style.color = "var(--mainColour)";
    document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
    document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
}
function mouseOver02() {
    document.querySelector("#text-link0").style.color = "var(--hoverColour)";
    document.querySelector("#text-link1").style.color = "var(--hoverColour)";
    document.querySelector("#text-link2").style.color = "var(--hoverColour)";
    document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
    document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
}
function mouseOut02() {
    document.querySelector("#text-link0").style.color = "var(--mainColour)";
    document.querySelector("#text-link1").style.color = "var(--mainColour)";
    document.querySelector("#text-link2").style.color = "var(--mainColour)";
    document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
    document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
}
