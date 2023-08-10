$(document).ready(function() {
    let i;
    const toggler = document.getElementsByClassName("caret");
    for (i = 0; i < toggler.length; i++) {
      toggler[i].addEventListener("click", function() {
        this.parentElement.querySelector(".nested").classList.toggle("active");
        this.classList.toggle("caret-down");
      });
    }

    $('#taxonomy-tree input[type="checkbox"]').change(updateTreeSelection);
});

function updateTreeSelection() {
    const selected = $('#taxonomy-tree input[type="checkbox"]:checked');
    const count = selected.length;
    $('#matrixCount span').text(count);
    if (count) {
        $('#matrixCount').addClass('text-success');
        $('#matrixCount').removeClass('text-danger');
    } else {
        $('#matrixCount').addClass('text-danger');
        $('#matrixCount').removeClass('text-success');
    }
}

function clearTreeSelection() {
    $('#taxonomy-tree input[type="checkbox"]:checked').prop('checked', false);
    updateTreeSelection();
}

function resetTreeList() {
    const toggler = document.getElementsByClassName("caret");
    for (i = 0; i < toggler.length; i++) {
      toggler[i].parentElement.querySelector(".nested").classList.remove("active");
      toggler[i].classList.remove("caret-down");
    }
}
