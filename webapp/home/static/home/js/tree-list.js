$(document).ready(function() {
    let i;
    const toggler = document.getElementsByClassName("caret");
    for (i = 0; i < toggler.length; i++) {
      toggler[i].addEventListener("click", function() {
        this.parentElement.querySelector(".nested").classList.toggle("active");
        this.classList.toggle("caret-down");
      });
    }
});
