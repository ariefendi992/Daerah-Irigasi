// header scroll
const header = document.getElementById("header");

// window.addEventListener("scroll", () => {
//   if (window.scrollY > 100) {
//     // header.classList.replace("sticky", "fixed");
//     header.classList.toggle('a');

//     // header.classList.add("top-0");
//   } else {
//     header.classList.replace("fixed", "sticky");
//     // header.classList.remove("top-0");
//   }
// });

// swiper js
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

// SHOW MENU
const showMenu = (toggleId, navId = null) => {
  const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId),
    burger = document.getElementById("burger-menu"),
    close = document.getElementById("close-menu");

  toggle.addEventListener("click", (e) => {
    e.preventDefault();
    nav.classList.toggle("visible");
    nav.classList.toggle("scale-y-100");
    nav.classList.toggle("opacity-100");
    burger.classList.toggle("opacity-0");
    burger.classList.toggle("rotate-90");
    close.classList.toggle("opacity-100");
    close.classList.toggle("rotate-90");
  });
};

showMenu("nav-toggle", "nav-menu");

const navBtnMobile = document.querySelectorAll(".nav-menu-link-mobile");

navBtnMobile.forEach((btn) => {
  btn.addEventListener("click", (e) => {
    e.stopPropagation();

    const dropdonMoblie = btn.nextElementSibling;

    document.querySelectorAll(".dropdown-menu-mobile").forEach((menu) => {
      if (menu !== dropdonMoblie) {
        menu.classList.remove("menu-open");
      }
    });
    dropdonMoblie.classList.toggle("menu-open");
  });
});

// const showDropdownMenu = (menuItemId, subMenuItemId, iconDataId = null) => {
//   const menuItem = document.getElementById(menuItemId),
//     subMenuItem = document.getElementById(subMenuItemId),
//     iconData = document.getElementById(iconDataId);

//   menuItem.addEventListener("click", () => {
//     subMenuItem.classList.toggle("visible");
//     subMenuItem.classList.toggle("relative");
//     // iconData.classList.toggle("rotate-180");
//   });
// };

// showDropdownMenu("menu-item", "submenu-item", "icon-data");

// const menuParents = document.querySelectorAll(".has-submenu > div");
// const submenuParents = document.querySelectorAll(".has-subsubmenu > div");

// menuParents.forEach((menu) => {
//   const submenu = menu.nextElementSibling;

//   menu.addEventListener("click", () => {
//     submenu.classList.toggle("invisible");
//     submenu.classList.toggle("relative");

//     document.querySelectorAll(".has-submenu ul").forEach((ul) => {
//       if (ul !== submenu) {
//         ul.classList.add("invisible");
//         ul.classList.replace("relative", "absolute");
//       }
//     });
//   });
// });

// submenuParents.forEach((menu) => {
//   const subsubmenu = menu.nextElementSibling;

//   mmenu.addEventListener("click", (e) => {
//     if (window.innerWidth < 768) {
//       e.preventDefault();

//       // Tutup semua sub-submenu lain di level yang sama
//       const parent = menu.closest(".has-submenu");
//       parent.querySelectorAll(".has-subsubmenu > ul").forEach((ul) => {
//         if (ul !== subsubmenu) ul.classList.add("invisible");
//       });

//       subsubmenu.classList.toggle("invisible");
//     }
//   });
// });
