import { Application } from '@splinetool/runtime';

const canvas = document.getElementById('canvas3d');
const app = new Application(canvas);
app.load('https://prod.spline.design/tbWXvuEYkNG6dv3B/scene.splinecode').then(() => {
    canvas.classList.add('loaded');
});


// Настройки
const fadeOutHeight = 350;
let lastKnownScrollPosition = 0;
let ticking = false;

function updateCanvasOpacity(scrollPos) {
  const opacity = 1 - (scrollPos / fadeOutHeight);
  canvas.style.opacity = Math.max(opacity, 0);
}

window.addEventListener('scroll', function(e) {
  lastKnownScrollPosition = window.scrollY;

  if (!ticking) {
    window.requestAnimationFrame(function() {
      updateCanvasOpacity(lastKnownScrollPosition);
      ticking = false;
    });

    ticking = true;
  }
});
