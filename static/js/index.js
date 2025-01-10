// Array of text displayed in the page-load animation
var textArray = ['\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n<span class="red line1">const</span> <span class="darkblue line1">me</span> <span class="red line1">=</span> <span class="blue line1">"Matthew Moonen"</span><span class="white line1">;</span>', '\n<span class="red line2">let</span> <span class="white line2">you</span> <span class="red line2">=</span> <span class="blue line2">"visitor"</span><span class="white line2">;</span>', '\n\n<span class="purple line3">greetings</span><span class="darkblue line3">()</span><span class="white line3">;</span>', '\n\n<span class="red italic-code line4">async function</span> <span class="purple line4">greetings</span><span class="darkblue line4">() {</span>\n<span class="grey line5">••</span><span class="darkblue line5">console</span><span class="white line5">.</span><span class="purple line5">log</span><span class="orange line5">(</span><span class="blue line5">`Welcome</span> <span class="purple line5">${</span><span class="darkblue line5">you</span><span class="purple line5">}</span><span class="blue line5">!`</span><span class="orange line5">)</span><span class="white line5">;</span>\n<span class="grey line6">••</span><span class="red italic-code line6">await new</span> <span class="darkblue line6">Promise</span><span class="orange line6">(</span><span class="purple line6">(resolve)</span> <span class="red line6">=></span> <span class="purple line6">{</span>\n<span class="grey line7">••••</span><span class="darkblue line7">window</span><span class="white line7">.</span><span class="purple line7">addEventListener</span><span class="darkblue line7">(</span><span class="blue line7">"scroll"</span><span class="white line7">,</span> <span class="orange line7">()</span> <span class="red line7">=></span> <span class="orange line7">{</span>\n<span class="grey line8">••••••</span><span class="red line8">const</span> <span class="purple line8">{</span>\n<span class="grey line9">••••••••</span><span class="darkblue line9">scrollTop</span><span class="white line9">,</span>\n<span class="grey line10">••••••••</span><span class="darkblue line10">scrollHeight</span><span class="white line10">,</span>\n<span class="grey line11">••••••••</span><span class="darkblue line11">clientHeight</span>\n<span class="grey line12">••••••</span><span class="purple line12">}</span> <span class="red line12">=</span> <span class="darkblue line12">document</span><span class="white line12">.</span><span class="darkblue line12">documentElement</span><span class="white line12">;</span>\n<span class="grey line13">••••••</span><span class="red line13">if</span> <span class="purple line13">(</span><span class="darkblue line13">scrollTop</span> <span class="red line13">+</span> <span class="darkblue line13">clientHeight</span> <span class="red line13">=></span> <span class="darkblue line13">scrollHeight</span><span class="purple line13">) {</span>\n<span class="grey line14">••••••••</span><span class="purple line14">resolve</span><span class="darkblue line14">()</span><span class="white line14">;</span>\n<span class="grey line15">••••••</span><span class="purple line15">}</span>\n<span class="grey line16">••••</span><span class="orange line16">}</span><span class="darkblue line16">)</span><span class="white line16">;</span>\n<span class="grey line17">••</span><span class="purple line17">}</span><span class="orange line17">)</span><span class="white line17">;</span>\n<span class="grey line18">••</span><span class="darkblue line18">console</span><span class="white line18">.</span><span class="purple line18">log</span><span class="orange line18">(</span><span class="blue line18">Thanks for stopping by</span> <span class="purple line18">${</span><span class="darkblue line18">me</span><span class="purple line18">}</span><span class="blue line18">\'s website!</span><span class="orange line18">)</span><span class="white line18">;</span>\n<span class="darkblue line19">}</span>']

var animationText = document.getElementById("animation-text");

/* Declare element count as a variable which refers to the index of the above array.
   The animation speed and delay of each array element is controlled individually within the addElements() function below */
var elementCount = 0;

addElements();
	window.onload = function() {
    window.scrollTo(0, 0);
		setTimeout(function() {
			var restOfPageElements = document.querySelectorAll(".index-section");
			for (var i = 0; i < restOfPageElements.length; i++) {
				restOfPageElements[i].style.visibility = "visible";
			}
      document.body.style.overflow = "auto";
		}, 4250); // time in milliseconds after which the title page will be displayed
	};


function fadeInTitle() { // Fades title section in on load.
  // Get relevant div elements by ID.
  const pageTitle = document.getElementById("page-title");
  const promise = document.querySelector(".promise");
  const functionLine1 = document.querySelector('#function-line1');

  // Set initial opactity of elements in page title to 0
  pageTitle.style.opacity = 0;
  promise.style.opacity = 0;
  functionLine1.style.opacity = 0;

  setTimeout(() => { // Wait for 6 seconds before showing title page (whilst animation occurs)
    // Use the CSS transition property to fade in the elements over 2 seconds with an ease-in-out animation
    pageTitle.style.transition = "opacity 1s ease-in";
    pageTitle.style.opacity = 1;
    promise.style.transition = "opacity 3s ease-in";
    promise.style.opacity = 1;
    functionLine1.style.transition = "opacity 5s ease-in"
    functionLine1.style.opacity = 0.6;
  }, 6000);
}
window.addEventListener("load", fadeInTitle); // Call the function on page load



function fadeInNavbar() { // Fades navbar in on load.

  const div = document.querySelector(".navbar"); // Get the navbar by its class
  const body = document.body // Get whole document body as variable - function makes whole page navigable simultaneously when the navbar is shown

  
  div.style.opacity = 0; // Set title section div's initial opacity to 0
  body.style.backgroundColor = "rgb(33, 33, 33)" // Set colour of body background and title section background to match on load.
  div.style.backgroundColor = "rgb(33, 33, 33)"

  // body.style.backgroundColor = "white" 
  // div.style.backgroundColor = "white"




  // Wait for _ seconds
  setTimeout(() => {
    // Use the CSS transition property to fade in the div over 2 seconds with an ease-in-out animation
    div.style.visibility = "visible"
    div.style.backgroundColor = "hsla(207, 13%, 17%, 0.672)"
    body.style.backgroundColor = "hsl(207, 13%, 17%)" // Change colour of page's main background after navbar appears.

    // div.style.backgroundColor = "white"
    // body.style.backgroundColor = "white" // Change colour of page's main background after navbar appears.

    div.style.transition = "opacity 1s ease-in";
    div.style.opacity = 1;
  }, 4000);
}
window.addEventListener("load", fadeInNavbar) // Call the function on page load



function addElements() {

  var text = textArray[elementCount];
  var index = 0;
  var interval;
  var waitTime;

  if (elementCount <= 2) {
    waitTime = 600;
    interval = setInterval(addLetter, 20);
  } else if (elementCount === 2) {
    showTitle();
    waitTime = 200;
    interval = setInterval(addLetter, 8);
} else if (elementCount === 3) {
    waitTime = 0;
    interval = setInterval(addLetter, 5);
  } 

  function addLetter() {
    // Get the current character
    var char = text.charAt(index);

    /* The following lines extract <span> tags and class names from the array and adds them as HTML elements to the DOM.
       Colour/styling of the elements has been pre-added to the index.css file. The colours/stylings match the VS Code theme "Github Dark".
       To add additional code to the array, copy/paste the parsed code into VS Code and style each line as appropriate.
       Each line has an added class name, which allows fade animations per line. */

    if (char === "<") { // Check if the current character is the start of a tag
      var endIndex = text.indexOf(">", index); // Get index position of the end of the tag
      if (endIndex !== -1) {
        // Extract the tag and its contents
        var tag = text.slice(index, endIndex + 1);
        var contents = text.slice(index + tag.length, endIndex); //Get tag's inner text content and save as a variable.

        var newElement = document.createElement("span"); // Create a new element and add it to the HTML.
        if (tag.includes("class")) {
          // Set the class attribute if present
          var className = tag.match(/class=['"]([^'"]+)['"]/)[1];
          newElement.setAttribute("class", className);
        }
        newElement.textContent = contents; //
        animationText.appendChild(newElement);

        // Increment the index past the tag and its contents
        index = endIndex + 1;
      }
    } else {
      // Add the current character to the HTML element
      var lastChild = animationText.lastChild;
      if (lastChild && lastChild.nodeType === Node.ELEMENT_NODE && lastChild.tagName === "SPAN") {
        // Add the current character to the last span element
        lastChild.textContent += char;
      } else {
        // Create a new span element and add it to the HTML element
        var newElement = document.createElement("span");
        newElement.textContent = char;
        animationText.appendChild(newElement);
      }

      // Increment the index
      index++;
    }


    animationText.scrollTop = animationText.scrollHeight;
    // If all letters have been added, stop the interval and add the cursor
    if (index >= text.length) {
        clearInterval(interval);
        animationText.insertAdjacentHTML("beforeend", '<span class="cursor">|</span>');
        
        setTimeout(function() { // Remove the cursor after 5 seconds
            var cursor = animationText.querySelector('.cursor');
            cursor.parentNode.removeChild(cursor);
        elementCount++;
        addElements();
      }, waitTime);
    }
  }
}