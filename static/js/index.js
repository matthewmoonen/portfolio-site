var textArray = ['\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n<span class="red line1">const</span> <span class="darkblue line1">me</span> <span class="red line1">=</span> <span class="blue line1">"Matthew Moonen"</span><span class="white line1">;</span>', '\n<span class="red line2">let</span> <span class="white line2">you</span> <span class="red line2">=</span> <span class="blue line2">"visitor"</span><span class="white line2">;</span>', '\n\n<span class="purple line3">greetings</span><span class="darkblue line3">()</span><span class="white line3">;</span>', '\n\n<span class="red italic-code line4">async function</span> <span class="purple line4">greetings</span><span class="darkblue line4">() {</span>\n<span class="grey line5">••</span><span class="darkblue line5">console</span><span class="white line5">.</span><span class="purple line5">log</span><span class="orange line5">(</span><span class="blue line5">`Welcome</span> <span class="purple line5">${</span><span class="darkblue line5">you</span><span class="purple line5">}</span><span class="blue line5">!`</span><span class="orange line5">)</span><span class="white line5">;</span>\n<span class="grey line6">••</span><span class="red italic-code line6">await new</span> <span class="darkblue line6">Promise</span><span class="orange line6">(</span><span class="purple line6">(resolve)</span> <span class="red line6">=></span> <span class="purple line6">{</span>\n<span class="grey line7">••••</span><span class="darkblue line7">window</span><span class="white line7">.</span><span class="purple line7">addEventListener</span><span class="darkblue line7">(</span><span class="blue line7">"scroll"</span><span class="white line7">,</span> <span class="orange line7">()</span> <span class="red line7">=></span> <span class="orange line7">{</span>\n<span class="grey line8">••••••</span><span class="red line8">const</span> <span class="purple line8">{</span>\n<span class="grey line9">••••••••</span><span class="darkblue line9">scrollTop</span><span class="white line9">,</span>\n<span class="grey line10">••••••••</span><span class="darkblue line10">scrollHeight</span><span class="white line10">,</span>\n<span class="grey line11">••••••••</span><span class="darkblue line11">clientHeight</span>\n<span class="grey line12">••••••</span><span class="purple line12">}</span> <span class="red line12">=</span> <span class="darkblue line12">document</span><span class="white line12">.</span><span class="darkblue line12">documentElement</span><span class="white line12">;</span>\n<span class="grey line13">••••••</span><span class="red line13">if</span> <span class="purple line13">(</span><span class="darkblue line13">scrollTop</span> <span class="red line13">+</span> <span class="darkblue line13">clientHeight</span> <span class="red line13">=></span> <span class="darkblue line13">scrollHeight</span><span class="purple line13">) {</span>\n<span class="grey line14">••••••••</span><span class="purple line14">resolve</span><span class="darkblue line14">()</span><span class="white line14">;</span>\n<span class="grey line15">••••••</span><span class="purple line15">}</span>\n<span class="grey line16">••••</span><span class="orange line16">}</span><span class="darkblue line16">)</span><span class="white line16">;</span>\n<span class="grey line17">••</span><span class="purple line17">}</span><span class="orange line17">)</span><span class="white line17">;</span>\n<span class="grey line18">••</span><span class="darkblue line18">console</span><span class="white line18">.</span><span class="purple line18">log</span><span class="orange line18">(</span><span class="blue line18">Thanks for stopping by</span> <span class="purple line18">${</span><span class="darkblue line18">me</span><span class="purple line18">}</span><span class="blue line18">\'s website!</span><span class="orange line18">)</span><span class="white line18">;</span>\n<span class="darkblue line19">}</span>']


var element = document.getElementById("text");
var elementCount = 0;

addElements();
// triggerEndAnimation()

// body.style.maxHeight = "100vh"
// body.style.overflow = "hidden"


// window.onload = function() {
//   setTimeout(function() {
//     document.querySelector(".index-section").style.display = "block";
//   }, 5000); // 5000 is the time in milliseconds (5 seconds) after which the rest of the page will be displayed
// };


	window.onload = function() {
    window.scrollTo(0, 0);
		setTimeout(function() {
			var restOfPageElements = document.querySelectorAll(".index-section");
			for (var i = 0; i < restOfPageElements.length; i++) {
				restOfPageElements[i].style.visibility = "visible";
			}
      document.body.style.overflow = "auto";
      // document.querySelector(".promise").style.visibility = "visible"
		}, 5000); // 5000 is the time in milliseconds (5 seconds) after which the rest of the page will be displayed
	};






function fadeInTitle() {
  // Get the div element by its ID
  const pageTitle = document.getElementById("page-title");
  const promise = document.querySelector(".promise");
  const functionLine1 = document.querySelector('#asdf');
  // const functionLine2 = document.querySelector('.line2');
  // const functionLine3 = document.querySelector('.line3');
  // const functionLine4 = document.querySelector('.line4');
  // const functionLine5 = document.querySelector('.line5');


  // Set the pageTitle's initial opacity to 0
  pageTitle.style.opacity = 0;
  promise.style.opacity = 0;
  functionLine1.style.opacity = 0;



  // Wait for 5 seconds
  setTimeout(() => {
    // Use the CSS transition property to fade in the pageTitle over 2 seconds with an ease-in-out animation
    pageTitle.style.transition = "opacity 1s ease-in";
    pageTitle.style.opacity = 1;
    promise.style.transition = "opacity 3s ease-in";
    promise.style.opacity = 1;
    functionLine1.style.transition = "opacity 5s ease-in"
    functionLine1.style.opacity = 0.6;
    // functionLine2.style.transition = "opacity 1s ease-out"
    // functionLine2.style.opacity = 0.2;
    // functionLine3.style.transition = "opacity 1s ease-out"
    // functionLine3.style.opacity = 0.2;
    // functionLine4.style.transition = "opacity 1s ease-out"
    // functionLine4.style.opacity = 0.2;
    // functionLine5.style.transition = "opacity 1s ease-out"
    // functionLine5.style.opacity = 0.2;
  }, 6000);
}

// Call the function on page load
window.addEventListener("load", fadeInTitle);




function fadeInNavbar() {
  // Get the div element by its ID
  const div = document.querySelector(".navbar");
  const body = document.body
  // const indexPageSections = document.querySelector(".index-section")
  // const promiseSection = document.querySelector(".promise-section");

  


  // Set the div's initial opacity to 0
  div.style.opacity = 0;
  body.style.backgroundColor = "rgb(33, 33, 33)"
  div.style.backgroundColor = "rgb(33, 33, 33)"

  // Wait for 5 seconds
  setTimeout(() => {
    // Use the CSS transition property to fade in the div over 2 seconds with an ease-in-out animation
    div.style.visibility = "visible"
    div.style.backgroundColor = "hsla(207, 13%, 17%, 0.672)"
    body.style.backgroundColor = "hsl(207, 13%, 17%)"
    div.style.transition = "opacity 1s ease-in";
    div.style.opacity = 1;
    body.style.backgroundColor = "hsl(207, 13%, 17%)"
  }, 5000);
}

window.addEventListener("load", fadeInNavbar)



function addElements() {
  // var text = textArray[elementCount].replace(/\n/g, "<br>");
  var text = textArray[elementCount];
  var index = 0;
  var interval;
  var waitTime;
  var homeTopHalf = document.querySelector("#text")
  var endAnimation = false

  if (elementCount <= 2) {
    waitTime = 600;
    interval = setInterval(addLetter, 20);
  } else if (elementCount === 2) {
    showTitle();
    waitTime = 200;
    // fadeOut = true;
    endAnimation = true;
    // triggerEndAnimation()
    interval = setInterval(addLetter, 8);
} else if (elementCount === 3) {
    waitTime = 0;
    // fadeOut = true;
    interval = setInterval(addLetter, 5);
  } 

  function addLetter() {
    // Get the current character
    var char = text.charAt(index);

    // Check if the current character is the start of a tag
    if (char === "<") {
      // Get the end of the tag
      var endIndex = text.indexOf(">", index);
      if (endIndex !== -1) {
        // Extract the tag and its contents
        var tag = text.slice(index, endIndex + 1);
        var contents = text.slice(index + tag.length, endIndex);

        // Create a new element and add it to the HTML element
        var newElement = document.createElement("span");
        if (tag.includes("class")) {
          // Set the class attribute if present
          var className = tag.match(/class=['"]([^'"]+)['"]/)[1];
          newElement.setAttribute("class", className);
        }
        newElement.textContent = contents;
        element.appendChild(newElement);

        // Increment the index past the tag and its contents
        index = endIndex + 1;
      }
    } else {
      // Add the current character to the HTML element
      var lastChild = element.lastChild;
      if (lastChild && lastChild.nodeType === Node.ELEMENT_NODE && lastChild.tagName === "SPAN") {
        // Add the current character to the last span element
        lastChild.textContent += char;
      } else {
        // Create a new span element and add it to the HTML element
        var newElement = document.createElement("span");
        newElement.textContent = char;
        element.appendChild(newElement);
      }

      // Increment the index
      index++;
    }


    
    element.scrollTop = element.scrollHeight;
    // If all letters have been added, stop the interval and add the cursor
    if (index >= text.length) {
        clearInterval(interval);
        element.insertAdjacentHTML("beforeend", '<span class="cursor">|</span>');
        // Remove the cursor after 5 seconds
        setTimeout(function() {
            var cursor = element.querySelector('.cursor');
            cursor.parentNode.removeChild(cursor);
        elementCount++;
        addElements();
      }, waitTime);
    }
  }
}



function triggerFadeOut(element) {
    let opacity = 1;
    function animate() {
      opacity -= 0.1;
      element.style.opacity = opacity;
      if(opacity <= 0) {
        element.style.display = 'none';
      } else {
        requestAnimationFrame(animate);
      }
    }
    requestAnimationFrame(animate);
  }
  




// function triggerFadeOut(topHalfHome) {
//     let opacity = 1;
//     const timer = setInterval(function() {
//       if(opacity <= 0.1) {
//         clearInterval(timer);
//         topHalfHome.style.opacity = 0;
//         topHalfHome.style.display = 'none';
//       }
//       topHalfHome.style.opacity = opacity;
//       opacity -= 0.1;
//     }, 10);
//   }
  


// function triggerFadeOut(topHalfHome) {
//   let opacity = 1;
//   const timer = setInterval(function() {
//     if(opacity <= 0.1) {
//       clearInterval(timer);
//       topHalfHome.style.display = 'none';
//     }
//     topHalfHome.style.opacity = opacity;
//     opacity -= 0.1;
//   }, 50);
// }








function triggerEndAnimation() {
  console.log('triggered');
    setTimeout(() => {
    const div = document.getElementById("text");
    div.style.transition = "transform 5s ease-out";
    div.style.transform = "translateY(-1500px)";
    }, 5000);
}
