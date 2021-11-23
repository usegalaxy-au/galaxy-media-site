// Prettify JSON fields

(function($) {
  $(document).ready( () => {
    el = document.getElementById('id_address')
    el.value = JSON.stringify(JSON.parse(el.value), null, 4)
    el.setAttribute('style', 'font-family: monospace;')
  });
})(django.jQuery);
