// TODO: on load, set value of terms statement
// TODO: on load, set value of matrices
// TODO: scroll to backend errors on load

$(document).ready(function() {
  setMatricesValue();
  setTermsValue();
  addTreeBranchClickEvent();
  $('#taxonomy-tree input[type="checkbox"]').change(updateTreeSelection);
});

function addTreeBranchClickEvent() {
  let i;
  const toggler = document.getElementsByClassName("caret");
  for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", function() {
      this.parentElement.querySelector(".nested").classList.toggle("active");
      this.classList.toggle("caret-down");
    });
  }
}

function setMatricesValue() {
  const matricesValueText = $('#matricesValue').text().replaceAll("'", '"');
  const selectedMatrices = JSON.parse(matricesValueText);
  if (selectedMatrices.length) {
    selectedMatrices.forEach( (value) => {
        $(`#taxonomy-tree input[type="checkbox"][value="${value}"]`)
          .prop('checked', true);
    });
    updateTreeSelection();
  }
}

function setTermsValue() {
  $('#agreeTermsInput').is(':checked')
  && $('#termsModal')
    .siblings('.form-check')
    .css('visibility', 'visible');
}

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
