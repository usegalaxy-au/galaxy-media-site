// Add markdown editor to the "body" field in django admin

window.onload = () => {
  var simplemde = new SimpleMDE({
    element: document.getElementById("id_body")
  });
};
