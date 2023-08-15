$(document).ready(function() {
  setMatricesValue();
  setTermsValue();
  addTreeBranchClickEvent();
  scrollToErrors();
  // Add event handler to update "selected matrices" count
  $('#taxonomy-tree input[type="checkbox"]').change(updateTreeSelection);
});

const debouncedSearchTree = (q) => _.debounce(
  // Debounce to prevent rapid firing while user types
  () => searchTree(q),
  500,
  { 'leading': true, 'trailing': false },
)();

function searchTree(query) {
  resetTreeList();
  if (!query) return;
  let exit = false;
  const matched = [];
  const choices = $('#taxonomy-tree span.choice');
  choices.each( (i, node) => {
    if (exit) return;
    const text = $(node).find('label').text();
    if (text.toLowerCase().indexOf(query.toLowerCase()) > -1) {
      const input_id = $(node).find('input').val();
      matched.push({node: node, label: text, id: input_id});
    }
  });
  showTreeMatches(matched);
}

function showTreeMatches(matched) {
  dropdown = $('#treeSearch .dropdown');
  dropdown.empty();
  matched.forEach( (match) => {
    const option = $(`
      <option onclick="selectTreeMatch('${match.id}');">
        ${match.label}
      </option>`);
    dropdown.append(option);
  });
  // Add click handler to body to close dropdown when clicking outside treeSearch
  $('body').click( (e) => {
    if ( !$(e.target).closest('#treeSearch').length) {
      dropdown.empty();
    }
  });
}

function selectTreeMatch(id) {
  $('#treeSearch .dropdown').empty();
  const input = $(`#taxonomy-tree input[value="${id}"]`);
  input.prop('checked', true);
  let parent = input.closest('ul');
  while (parent.hasClass('nested')) {
    parent.siblings('.caret').click();
    parent = $(parent).parent().parent();
  }
  updateTreeSelection();
}

function scrollToErrors() {
  const errors = $('.errorlist');
  if (errors.length) {
    const top = errors.offset().top;
    $('html, body').animate({scrollTop: top - 80}, 500);
  }
}

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
  $('#treeSearch input').val('');
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
