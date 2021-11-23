// Add markdown editor to the "body" field in django admin

(function($) {
  $(document).ready( () => {
    var simplemde = new SimpleMDE({
      element: document.getElementById("id_body")
    });
  });
})(django.jQuery);
