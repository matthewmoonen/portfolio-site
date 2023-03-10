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

// Define smooth scrolling behavior for navbar links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();

        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});




// // Define fade-in behavior for sections
// document.addEventListener('scroll', function() {
//     let homeSection = document.querySelectorAll('.index-home');

//     homeSection.forEach(homeSection => {
//         let homeSectionTop = homeSection.getBoundingClientRect().top;
//         let homeSectionBottom = homeSection.getBoundingClientRect().bottom;
//         let homeSectionHeight = homeSection.getBoundingClientRect().height;

//         if (homeSectionTop < window.innerHeight && homeSectionBottom >= 0) {
//             homeSection.classList.add('active');
//         } 
//         else if (homeSectionTop < window.innerHeight - homeSectionHeight) {
//             homeSection.classList.remove('active');
//         }
//     });




//     const sections = document.querySelectorAll('.index-section');

//     const isInViewport = (element) => {
//       const { top, bottom, height } = element.getBoundingClientRect();
//       return top < window.innerHeight && bottom >= 0 && height > 0;
//     };
    
//     sections.forEach((section) => {
//       if (isInViewport(section)) {
//         section.classList.add('active');
//       } else {
//         section.classList.remove('active');
//       }
//     });
    




//     // let sections = document.querySelectorAll('.index-section');

//     // sections.forEach(section => {
//     //     let sectionTop = section.getBoundingClientRect().top;
//     //     let sectionBottom = section.getBoundingClientRect().bottom;
//     //     let sectionHeight = section.getBoundingClientRect().height;

//     //     if (sectionTop < window.innerHeight && sectionBottom >= 0) {
//     //         section.classList.add('active');
//     //     } 
//     //     else if (sectionTop < window.innerHeight - sectionHeight) {
//     //         section.classList.remove('active');
//     //     }
//     // });
// });








const isInViewport = (element) => {
    const { top, bottom, height } = element.getBoundingClientRect();
    return top < window.innerHeight && bottom >= 0 && height > 0;
  };
  
  const handleScroll = () => {
    const sections = document.querySelectorAll('.index-section');
    sections.forEach((section) => {
      if (isInViewport(section)) {
        section.classList.add('active');
      } else {
        section.classList.remove('active');
      }
    });
  };
  
  // Call handleScroll initially to set active classes on load
  handleScroll();
  
  document.addEventListener('scroll', handleScroll);
  