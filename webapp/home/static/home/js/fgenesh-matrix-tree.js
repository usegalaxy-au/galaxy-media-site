const SELECTION_ENABLED = false;

$(document).ready(function() {
  setTermsValue();
  addNodeClickEvent();

  if (SELECTION_ENABLED) {
    setMatricesValue();
    // Add event handler to update "selected matrices" count
    $('#taxonomy-tree input[type="checkbox"]').change(updateTreeSelection);
  }
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

function expandTreeSelected() {
  const selected = $('#taxonomy-tree input:checked');
  if (selected.length) {
    selected.each( (i, node) => {
      const ul = $(node).closest('ul');
      expandTreeBranch(ul);
    });
  }
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
  SELECTION_ENABLED && input.prop('checked', true);
  let ul = input.closest('ul');
  expandTreeBranch(ul);
  updateTreeSelection();
}

function expandTreeBranch(ul) {
  let parent = ul;
  while (parent.hasClass('nested')) {
    parent.siblings('.caret').not('.caret-down').click();
    parent = $(parent).parent().parent();
  }
}

function expandNode(node) {
  node.querySelector(".nested").classList.toggle("active");
  const nodeButton = node.querySelector(".caret");
  nodeButton.classList.toggle("caret-down");

  // if node has only one child, expand child too (recursive)
  const children = node.querySelector(".nested").children;
  children.length === 1 && expandNode(children[0]);
}

function addNodeClickEvent() {
  let i;
  const toggler = document.getElementsByClassName("caret");
  for (i = 0; i < toggler.length; i++) {
    toggler[i].addEventListener("click", (e) => expandNode(e.target.parentElement));
  }
}

function setMatricesValue() {
  if (!SELECTION_ENABLED) return;
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
  if (!SELECTION_ENABLED) return;
  const selected = $('#taxonomy-tree input:checked');
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
  if (!SELECTION_ENABLED) return;
  $('#treeSearch input').val('');
  $('#taxonomy-tree input:checked').prop('checked', false);
  updateTreeSelection();
}

function resetTreeList() {
    const toggler = document.getElementsByClassName("caret");
    for (i = 0; i < toggler.length; i++) {
      toggler[i].parentElement.querySelector(".nested").classList.remove("active");
      toggler[i].classList.remove("caret-down");
    }
}
