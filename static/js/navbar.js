function menuItemClick() {
  console.log('menuitemclicked')
  if (window.innerWidth < 992) {
    console.log('and its on mobile')
  }
}

function toggleMenuOn() {
    document.querySelector(".home").style.display = "none"
    document.querySelector(".toggle-on").style.display = "none"
    // document.querySelector(".hide-me").style.display = "block"
    document.querySelector("body").style.overflow = "hidden"
    document.querySelector(".toggle-off").style.display = "inline"
    
    const navbar = document.querySelector(".navbar")
    navbar.style.borderBottomWidth = "100vh";
    navbar.style.backgroundColor = "rgb(38, 44, 49)";
    navbar.style.borderBottomColor = "rgb(38, 44, 49)";
    
    document.querySelector(".navbar-links").style.display = "inline"
    const navbarLinks = document.querySelectorAll('.navbar-links a');
    navbarLinks.forEach(link => {
      setTimeout(() => {
        link.classList.toggle('active');
      }, 10);
    });
}

function toggleMenuOff() {

  if (window.innerWidth < 992) {
    const body = document.querySelector("body");
    body.style.overflow = "scroll";

    document.querySelector(".navbar").style.borderBottomWidth = "0px";

    document.querySelector(".hide-me").style.display = "none";
    document.querySelector(".navbar-links").style.display = "none";
    document.querySelector(".home").style.display = "inline";
    document.querySelector(".toggle-on").style.display = "inline"
    document.querySelector(".toggle-off").style.display = "none";
    document.querySelector(".navbar").style.backgroundColor = "rgba(38, 44, 49, 0.67)";


    const navbarLinks = document.querySelectorAll('.navbar-links a');
    navbarLinks.forEach(link => {
      link.classList.toggle('active');
    });

}
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
  



  function handleViewportChange() {
    // Get the current viewport width
    var viewportWidth = window.innerWidth || document.documentElement.clientWidth;
  
    if (viewportWidth >= 991) {
      
      document.querySelector(".navbar-links").style.display = "inline"
    } else {
      document.querySelector(".navbar-links").style.display = "none"
    }
  }
  
  // Attach the function to the window's resize event
  window.addEventListener("resize", handleViewportChange);
  