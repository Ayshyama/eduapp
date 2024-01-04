const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close');

// Function to check screen width and hide/show menu accordingly
const checkScreenWidth = () => {
    const screenWidth = window.innerWidth;

    if (screenWidth > 767) {
        navMenu.classList.remove('show-menu');
        navToggle.style.display = 'none';
        navClose.style.display = 'none';
    } else {
        navToggle.style.display = 'block';
    }
};

// Initial check on page load
checkScreenWidth();

// Listen for window resize event
window.addEventListener('resize', checkScreenWidth);

// MENU SHOW
if (navToggle) {
    navToggle.addEventListener('click', () => {
        if (navMenu.classList.contains('show-menu')) {
            navMenu.classList.remove('show-menu');
            navClose.style.display = 'none';
        } else {
            navMenu.classList.add('show-menu');
            navClose.style.display = 'block';
        }
    });
}

// MENU HIDDEN
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu');
        navClose.style.display = 'none';
    });
}

// REMOVE MENU MOBILE
const navLink = document.querySelectorAll('.nav__link');
const linkAction = () => {
    navMenu.classList.remove('show-menu');
    navClose.style.display = 'none';
};
navLink.forEach(n => n.addEventListener('click', linkAction));




const navMenuUser = document.getElementById('nav-menu-user');
const navCloseUser = document.getElementById('nav-close-user');
const navButtons = document.getElementById('nav-buttons');

// Function to open the user menu
const openUserMenu = () => {
    navMenuUser.classList.add('show-menu-user');
    navCloseUser.style.display = 'block';
};

// Event listener for opening the user menu when clicking on button__welcome
if (navButtons) {
    navButtons.addEventListener('click', openUserMenu);
}

// Function to close the user menu
const closeUserMenu = () => {
    // Wait for a short delay before removing the 'show-menu' class
    setTimeout(() => {
        navMenuUser.classList.remove('show-menu-user');
    }, 50);

    navCloseUser.style.display = 'none';
};

if (navCloseUser) {
    navCloseUser.addEventListener('click', closeUserMenu);
}

// REMOVE MENU MOBILE
const navLinkUser = document.querySelectorAll('.nav__link-user');
const linkActionUser = () => {
    navMenuUser.classList.remove('show-menu-user');
    navButtons.style.display = 'block';
    navCloseUser.style.display = 'none';
};
navLinkUser.forEach(n => n.addEventListener('click', linkActionUser));
