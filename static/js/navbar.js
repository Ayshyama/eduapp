// ----------------NAV MENU---------------- //
const navMenu = document.getElementById('nav-menu'),
    navToggle = document.getElementById('nav-toggle'),
    navClose = document.getElementById('nav-close');

// MENU SHOW
if (navToggle) {
    navToggle.addEventListener('click', () => {
        if (navMenu.classList.contains('show-menu')) {
            navMenu.classList.remove('show-menu');
            // navClose.style.display = 'none';
        } else {
            navMenu.classList.add('show-menu');
            navClose.style.display = 'flex';
        }
    });
}

// MENU HIDDEN
if (navClose) {
    navClose.addEventListener('click', () => {
        navMenu.classList.remove('show-menu');
        // navClose.style.display = 'none';
    });
}

// REMOVE MENU MOBILE
const navLink = document.querySelectorAll('.nav__link');
const linkAction = () => {
    navMenu.classList.remove('show-menu');
    // navClose.style.display = 'none';
};
navLink.forEach(n => n.addEventListener('click', linkAction));






// ----------------USER MENU---------------- //
const navMenuUser = document.getElementById('nav-menu-user');
const navCloseUser = document.getElementById('nav-close-user');
const navButtons = document.getElementById('auth-icon');

// Function to open the user menu
const openUserMenu = () => {
    navMenuUser.classList.add('show-menu-user');
    navCloseUser.style.display = 'flex';
};

// MENU SHOW
if (navButtons) {
    navButtons.addEventListener('click', openUserMenu);
}

// MENU HIDDEN
const closeUserMenu = () => {
    setTimeout(() => {
        navMenuUser.classList.remove('show-menu-user');
    }, 50);
    // navCloseUser.style.display = 'none';
};

if (navCloseUser) {
    navCloseUser.addEventListener('click', closeUserMenu);
}


// REMOVE MENU MOBILE
const navLinkUser = document.querySelectorAll('.nav__link-user');
const linkActionUser = () => {
    navMenuUser.classList.remove('show-menu-user');
    navButtons.style.display = 'flex';
    // navCloseUser.style.display = 'none';
};
navLinkUser.forEach(n => n.addEventListener('click', linkActionUser));









//Function to check screen width and hide/show menu accordingly
const checkScreenWidth = () => {
    const screenWidth = window.innerWidth;

    if (screenWidth > 1280) {
        navMenu.classList.remove('show-menu');
        navToggle.style.display = 'none';
        navClose.style.display = 'none';
        navCloseUser.style.display = 'none';
    } else {
        navToggle.style.display = 'flex';
    }
};

// Initial check on page load
checkScreenWidth();

// Listen for window resize event
window.addEventListener('resize', checkScreenWidth);

const debounce = (func, delay) => {
    let timeoutId;
    return () => {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(func, delay);
    };
};

// Debounced window resize event
window.addEventListener('resize', debounce(checkScreenWidth, 250));