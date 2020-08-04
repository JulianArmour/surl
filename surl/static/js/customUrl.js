const customBtn = document.getElementById("custom-btn");

function toggleCustom() {
    document.getElementById("custom-section").classList.remove("hidden-none");
    customBtn.classList.add("hidden-none")
}


customBtn.addEventListener("click", toggleCustom)