document.addEventListener('DOMContentLoaded', (event) => {
const sign_in_btn = document.querySelector("#sign-in-btn");
const sign_up_btn = document.querySelector("#sign-up-btn");
const container = document.querySelector(".container");

  sign_up_btn.addEventListener("click", () => {
    container.classList.remove("sign-in-mode");
    container.classList.add("sign-up-mode");
  });

  sign_in_btn.addEventListener("click", () => {
    container.classList.remove("sign-up-mode");
    container.classList.add("sign-in-mode");
  });

});

document.addEventListener('DOMContentLoaded', (event) => {
  const sign_in_btn = document.querySelector("#sign-in-btn");
  const sign_up_btn = document.querySelector("#sign-up-btn");
  const container = document.querySelector(".container");

    sign_up_btn.addEventListener('click', () => {
        container.classList.add("active");
    });

    sign_in_btn.addEventListener('click', () => {
        container.classList.remove("active");
    });

});

document.addEventListener('DOMContentLoaded', (event) => {
  const sign_in_btn = document.querySelector("#sign-in-btn");
  const sign_up_btn = document.querySelector("#sign-up-btn");
  const form = document.querySelector(".signin-signup");

  sign_up_btn.addEventListener('click', () => {
    fadeOut(form, () => {
      fadeIn(form);
    });
  });

  sign_in_btn.addEventListener('click', () => {
    fadeOut(form, () => {
      fadeIn(form);
    });
  });

  function fadeOut(element, callback) {
    element.style.opacity = 0;
    element.style.visibility = "visible";
    setTimeout(() => {
      callback();
    }, 500);
  }

  function fadeIn(element) {
    element.style.opacity = 1;
  }
});



