// Toggle Dark Mode
function toggleDarkMode() {
    document.body.classList.toggle("dark-mode");
    localStorage.setItem("darkMode", document.body.classList.contains("dark-mode"));
}

// Preserve Dark Mode on Page Load
window.onload = function () {
    if (localStorage.getItem("darkMode") === "true") {
        document.body.classList.add("dark-mode");
    }
};

// Toggle Collapsible Navbar
function toggleNavbar() {
    let nav = document.querySelector(".nav-links");
    nav.style.display = nav.style.display === "block" ? "none" : "block";
}
