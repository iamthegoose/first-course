window.addEventListener("scroll", function () {
  const header = document.getElementById("header");
  if (window.scrollY > 0) {
    header.classList.add("scrolled");
    header.classList.remove("top");
  } else {
    header.classList.add("top");
    header.classList.remove("scrolled");
  }
});

const token = localStorage.getItem("token");

function handleClick(e) {
  e.preventDefault();
  if (token) {
    window.location.href = "/rent";
  } else {
    window.location.href = "/login";
  }
}

function handleClickLink(e) {
  e.preventDefault();
  if (token) {
    window.location.href = "/create-flats";
  } else {
    window.location.href = "/login";
  }
}

const catalogue = document.getElementById("catalogueForm");
const itemRent = document.querySelector(".menu-item-rent");
const itemCreateRent = document.querySelector(".menu-item-create-rent");

catalogue.addEventListener("click", handleClick);
itemRent.addEventListener("click", handleClick);
itemCreateRent.addEventListener("click", itemClick);

// console.log("qweekrbj");

// const flatsItem = document.querySelector(".flats-item");
// console.log(flatsItem);
// flatsItem.addEventListener("click", itemClick);

// function itemClick() {
//   console.log("qwe");
//   const res = confirm("Орендувати цю квартиру?");
//   if (res) {
//     alert("Заявка подана успішно!");
//   } else {
//     return;
//   }
// }
