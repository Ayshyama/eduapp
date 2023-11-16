console.log("btn_animation.js is loaded");

// BUTTON ANIMATION from CHATGPT
let btn = document.querySelector('.hero__button');
let angle = 0;
let rafId; // RequestAnimationFrame ID

const updateGradient = () => {
  btn.style.setProperty('--x', angle + `deg`);
  angle = (angle + 1) % 360; // Increase the angle by 1 degree and wrap around at 360
  rafId = requestAnimationFrame(updateGradient);
};

// Start the animation immediately
rafId = requestAnimationFrame(updateGradient);
