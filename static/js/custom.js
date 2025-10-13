// header scroll
const header = document.getElementById("header");
window.addEventListener("scroll", () => {
  if (window.scrollY > 1) {
    header.classList.add("sticky");
    header.classList.add("top-0");
  } else {
    header.classList.remove("sticky");
    header.classList.remove("top-0");
  }
});

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
const showMenu = (toggleId, navId) => {
  const toggle = document.getElementById(toggleId),
    nav = document.getElementById(navId);

  toggle.addEventListener("click", () => {
    // Add show-menu close nav menu
    nav.classList.toggle("show-menu");
    nav.classList.toggle("left-0");
    // nav.classList.replace("left-0", "-left-full");
    // Add show-cion to show and hide menu icon
    toggle.classList.toggle("show-icon");
    // nav.classList.replace("-left-full", "left-0");
  });
};

showMenu("nav-toggle", "nav-menu");

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

const menuParents = document.querySelectorAll(".has-submenu > div");
const submenuParents = document.querySelectorAll(".has-subsubmenu > div");

menuParents.forEach((menu) => {
  const submenu = menu.nextElementSibling;

  menu.addEventListener("click", () => {
    submenu.classList.toggle("invisible");
    submenu.classList.toggle("relative");

    document.querySelectorAll(".has-submenu ul").forEach((ul) => {
      if (ul !== submenu) {
        ul.classList.add("invisible");
        ul.classList.replace("relative", "absolute");
      }
    });
  });
});

submenuParents.forEach((menu) => {
  const subsubmenu = menu.nextElementSibling;

  mmenu.addEventListener("click", (e) => {
    if (window.innerWidth < 768) {
      e.preventDefault();

      // Tutup semua sub-submenu lain di level yang sama
      const parent = menu.closest(".has-submenu");
      parent.querySelectorAll(".has-subsubmenu > ul").forEach((ul) => {
        if (ul !== subsubmenu) ul.classList.add("invisible");
      });

      subsubmenu.classList.toggle("invisible");
    }
  });
});
