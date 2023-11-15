console.log("navbar.js is loaded");                         // Check if the file is loaded


const navMenu = document.getElementById('nav-menu'),        // Get the menu
    navToggle = document.getElementById('nav-toggle'),      // Get the toggle button
    navClose = document.getElementById('nav-close');        // Get the close button


// MENU SHOW
if (navToggle) {                                    // If the toggle button exists
    navToggle.addEventListener('click', () => {     // When the toggle button is clicked
        navMenu.classList.add('show-menu');         // Show the menu
        navToggle.style.display = 'none';           // Hide the toggle button
        navClose.style.display = 'block';           // Show the close button
    });
}


// MENU HIDDEN
if (navClose) {                                     // If the close button exists
    navClose.addEventListener('click', () => {      // When the close button is clicked
        navMenu.classList.remove('show-menu');      // Hide the menu
        navToggle.style.display = 'block';          // Show the toggle button
        navClose.style.display = 'none';            // Hide the close button
    });
}


// REMOVE MENU MOBILE
const navLink = document.querySelectorAll('.nav__link');        // Get all the links
const linkAction = () => {                                      // When a link is clicked
    navMenu.classList.remove('show-menu');                      // Hide the menu
    navToggle.style.display = 'block';                          // Show the toggle button
    navClose.style.display = 'none';                            // Hide the close button
}
navLink.forEach(n => n.addEventListener('click', linkAction));  // Add the event listener to all the links






