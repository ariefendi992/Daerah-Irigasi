// const header = document.getElementById("header");

// window.addEventListener("scroll", () => {
//   if (window.scrollY > 1) {
//     header.classList.add("sticky");
//     header.classList.add("top-0");
//   } else {
//     header.classList.remove("sticky");
//     header.classList.remove("top-0");
//   }
// });
const swiper = new Swiper(".mySwiper", {
  loop: true,
  autoplay: {
    delay: 3500,
    disableOnInteraction: false,
  },
  pagination: {
    el: ".swiper-pagination",
  },
});
