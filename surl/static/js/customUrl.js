const customBtn = document.getElementById("custom-btn");
const customSection = document.getElementById("custom-section");
let customIsVisible = false;

function toggleCustom() {
    if (!customIsVisible) {
        customSection.classList.remove("hidden-none");
    } else {
        customSection.classList.add("hidden-none");
    }
    customIsVisible = !customIsVisible;
}

customBtn.addEventListener("click", toggleCustom);