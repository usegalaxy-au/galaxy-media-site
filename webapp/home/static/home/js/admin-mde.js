// Add markdown editor to the "body" field in django admin

(function($) {
  $(document).on('load', () => {
    var simplemde = new SimpleMDE({
      element: document.getElementById("id_body")
    });
  });
})(django.jQuery);
