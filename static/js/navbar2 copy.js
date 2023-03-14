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











// // THIS IS GOOD!
// const isInViewport = (element) => {
//     const { top, bottom, height } = element.getBoundingClientRect();
//     return top < window.innerHeight && bottom >= 0 && height > 0;
//   };
  
//   const handleScroll = () => {
//     const sections = document.querySelectorAll('.index-section');
//     sections.forEach((section) => {
//       if (isInViewport(section)) {
//         section.classList.add('active');
//       } else {
//         section.classList.remove('active');
//       }
//     });
//   };
  
//   // Call handleScroll initially to set active classes on load
//   handleScroll();
  
//   document.addEventListener('scroll', handleScroll);
  











// Niet zo goed!
// const isInViewport = (element) => {
//     const { top, bottom, height } = element.getBoundingClientRect();
//     return top < window.innerHeight && bottom >= 0 && height > 0;
//   };
  
//   const handleScroll = () => {
//     const sections = document.querySelectorAll('.index-section, .movement-transition');
//     sections.forEach((section) => {
//       if (isInViewport(section)) {
//         section.classList.add('active');
//       } else {
//         section.classList.remove('active');
//       }
//     });
//   };
  
//   // Call handleScroll initially to set active classes on load
//   handleScroll();
  
//   document.addEventListener('scroll', handleScroll);
  
//   const handleTransition = () => {
//     const transitions = document.querySelectorAll('.movement-transition');
//     transitions.forEach((transition) => {
//       if (isInViewport(transition)) {
//         transition.style.transform = 'translateY(0)';
//         transition.style.opacity = 1;
//         transition.style.transition = 'transform 1s ease-out, opacity 1s ease-out';
//       }
//     });
//   };
  
//   // Call handleTransition initially to set initial position
//   handleTransition();
  
//   document.addEventListener('scroll', handleTransition);
  




// const isInViewport = (element) => {
//     const { top, bottom, height } = element.getBoundingClientRect();
//     return top < window.innerHeight && bottom >= 0 && height > 0;
//   };
  
//   const handleScroll = () => {
//     const sections = document.querySelectorAll('.index-section, .movement-transition');
//     sections.forEach((section) => {
//       if (isInViewport(section)) {
//         section.classList.add('active');
//       } else {
//         section.classList.remove('active');
//       }
//     });
//   };
  
//   // Call handleScroll initially to set active classes on load
//   handleScroll();
  
//   document.addEventListener('scroll', () => {
//     handleScroll();
//     handleTransition();
//   });
  
//   const handleTransition = () => {
//     const transitions = document.querySelectorAll('.movement-transition');
//     transitions.forEach((transition) => {
//       if (isInViewport(transition)) {
//         transition.style.transform = 'translateY(0)';
//         transition.style.opacity = 1;
//         transition.style.transition = 'transform 1s ease-out, opacity 1s ease-out';
//       }
//     });
//   };
  










// const isInViewport = (element) => {
//     const { top, bottom, height } = element.getBoundingClientRect();
//     return top < window.innerHeight && bottom >= 0 && height > 0;
//   };
  
//   const handleScroll = () => {
//     const sections = document.querySelectorAll('.index-section, .movement-transition');
//     sections.forEach((section) => {
//       if (isInViewport(section)) {
//         section.classList.add('active');
//       } else {
//         section.classList.remove('active');
//       }
//     });
//   };
  
//   // Call handleScroll initially to set active classes on load
//   handleScroll();
  
//   document.addEventListener('scroll', () => {
//     handleScroll();
//     handleTransition();
//   });
  
//   const handleTransition = () => {
//     const transitions = document.querySelectorAll('.movement-transition.active');
//     transitions.forEach((transition) => {
//       if (isInViewport(transition)) {
//         transition.style.transform = 'translateY(0)';
//         transition.style.opacity = 1;
//         transition.style.transition = 'transform 1s ease-out, opacity 1s ease-out';
//       }
//     });
//   };
  











const isInViewport = (element) => {
    const { top, bottom, height } = element.getBoundingClientRect();
    return top < window.innerHeight && bottom >= 0 && height > 0;
  };
  
  const handleScroll = () => {
    const sections = document.querySelectorAll('.ismt');
    sections.forEach((section) => {
      if (isInViewport(section)) {
        section.classList.add('active');
      } 
      // UNCOMMENT to make elements move again on scroll.
      // else {
      //   section.classList.remove('active');
      // }
    });
  };
  
  // Call handleScroll initially to set active classes on load
  handleScroll();
  
  document.addEventListener('scroll', handleScroll);
  









// THIS IS GOOD!
const isInViewporta = (element) => {
    const { top, bottom, height } = element.getBoundingClientRect();
    return top < window.innerHeight && bottom >= 0 && height > 0;
  };
  
  const handleScrolla = () => {
    const sectionsa = document.querySelectorAll('.index-section');
    sectionsa.forEach((sectiona) => {
      if (isInViewporta(sectiona)) {
        sectiona.classList.add('active');
      } else {
        sectiona.classList.remove('active');
      }
    });
  };
  
  // Call handleScroll initially to set active classes on load
  handleScrolla();
  
  document.addEventListener('scroll', handleScrolla);
  
