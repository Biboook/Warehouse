const showPopupButton = document.getElementById("show-popup");
const closePopupButton = document.getElementById("close-popup");
const popup = document.querySelector(".popup");

showPopupButton.addEventListener("click", () => {
    popup.style.display = "block";
});

closePopupButton.addEventListener("click", () => {
    popup.style.display = "none";
});
