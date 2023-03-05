var bodyStyles = window.getComputedStyle(document.body);
var mainColour = bodyStyles.getPropertyValue('--mainColour')
var hoverColour = bodyStyles.getPropertyValue('--hoverColour')



let i = 0
var divs = document.querySelectorAll('.text-links a');
[].forEach.call(divs, function(div) {
    // console.log(div)
    // console.log(divs[i].id)
    eachLink(i, div, divs.length)
    i = i+1
    div.addEventListener("mouseenter", function( event ) {   
        event.target.style.color = "purple";
      }, false);
});

function eachLink(i, div, divslength) {
    for (j = 0; j < divslength; j++) {
        if (i !== j) {
            mydiv = '#text-link' + i;
            mydiv.addEventListener("mouseenter", function( event ) {   
                event.target.style.color = "purple";
            
              }, false);
        }
    }
    
    // console.log(i)
    // console.log(div)
    // console.log("heyyy")
}


















// var buttonNumber = "#text-link1"



// for (i = 0; i <= 3; i++) {
//     let buttonNumber = "#text-link1"
//     document.querySelector(buttonNumber).addEventListener("mouseover", mouseOver);
    
// }







// document.querySelector("#text-link0").addEventListener("mouseover", mouseOver0);
// document.querySelector("#text-link0").addEventListener("mouseout", mouseOut0);

// document.querySelector("#text-link0").addEventListener("mouseover", mouseOver0);
// document.querySelector("#text-link0").addEventListener("mouseout", mouseOut0);

// document.querySelector("#text-link1").addEventListener("mouseover", mouseOver1);
// document.querySelector("#text-link1").addEventListener("mouseout", mouseOut1);

// document.querySelector("#text-link2").addEventListener("mouseover", mouseOver2);
// document.querySelector("#text-link2").addEventListener("mouseout", mouseOut2);

// document.querySelector("#icon-link0").addEventListener("mouseover", mouseOver00);
// document.querySelector("#icon-link0").addEventListener("mouseout", mouseOut00);

// document.querySelector("#icon-link1").addEventListener("mouseover", mouseOver01);
// document.querySelector("#icon-link1").addEventListener("mouseout", mouseOut01);

// document.querySelector("#icon-link2").addEventListener("mouseover", mouseOver02);
// document.querySelector("#icon-link2").addEventListener("mouseout", mouseOut02);

// function mouseOver0() {
//     document.querySelector("#text-link1").style.color = "var(--hoverColour)";
//     document.querySelector("#text-link2").style.color = "var(--hoverColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
// }
// function mouseOut0() {
//     document.querySelector("#text-link1").style.color = "var(--mainColour)";
//     document.querySelector("#text-link2").style.color = "var(--mainColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
// }
// function mouseOver1() {
//     document.querySelector("#text-link0").style.color = "var(--hoverColour)";
//     document.querySelector("#text-link2").style.color = "var(--hoverColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
// }
// function mouseOut1() {
//     document.querySelector("#text-link0").style.color = "var(--mainColour)";
//     document.querySelector("#text-link2").style.color = "var(--mainColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
// }
// function mouseOver2() {
//     document.querySelector("#text-link0").style.color = "var(--hoverColour)";
//     document.querySelector("#text-link1").style.color = "var(--hoverColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
// }
// function mouseOut2() {
//     document.querySelector("#text-link0").style.color = "var(--mainColour)";
//     document.querySelector("#text-link1").style.color = "var(--mainColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
// }
// function mouseOver00() {
//     document.querySelector("#text-link0").style.color = "var(--hoverColour)";
//     document.querySelector("#text-link1").style.color = "var(--hoverColour)";
//     document.querySelector("#text-link2").style.color = "var(--hoverColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
// }
// function mouseOut00() {
//     document.querySelector("#text-link0").style.color = "var(--mainColour)";
//     document.querySelector("#text-link1").style.color = "var(--mainColour)";
//     document.querySelector("#text-link2").style.color = "var(--mainColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
// }

// function mouseOver01() {
//     document.querySelector("#text-link0").style.color = "var(--hoverColour)";
//     document.querySelector("#text-link1").style.color = "var(--hoverColour)";
//     document.querySelector("#text-link2").style.color = "var(--hoverColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--hoverColour)";
// }
// function mouseOut01() {
//     document.querySelector("#text-link0").style.color = "var(--mainColour)";
//     document.querySelector("#text-link1").style.color = "var(--mainColour)";
//     document.querySelector("#text-link2").style.color = "var(--mainColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
//     document.querySelector("#icon-link2").style.fill = "var(--mainColour)";
// }
// function mouseOver02() {
//     document.querySelector("#text-link0").style.color = "var(--hoverColour)";
//     document.querySelector("#text-link1").style.color = "var(--hoverColour)";
//     document.querySelector("#text-link2").style.color = "var(--hoverColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--hoverColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--hoverColour)";
// }
// function mouseOut02() {
//     document.querySelector("#text-link0").style.color = "var(--mainColour)";
//     document.querySelector("#text-link1").style.color = "var(--mainColour)";
//     document.querySelector("#text-link2").style.color = "var(--mainColour)";
//     document.querySelector("#icon-link0").style.fill = "var(--mainColour)";
//     document.querySelector("#icon-link1").style.fill = "var(--mainColour)";
// }