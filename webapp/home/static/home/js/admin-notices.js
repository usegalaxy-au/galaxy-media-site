(function($) {
  const setFormState = (image_class) => {
    if (image_class === 'none') {
      // Image class - hide redundant fields
      $('.field-static_display').hide();
      $('.field-display_title').hide();
      $('.field-short_description').hide();
      $('.field-material_icon').hide();
    } else {
      // Show fields
      $('.field-static_display').show();
      $('.field-display_title').show();
      $('.field-short_description').show();
      $('.field-material_icon').show();
    }
  }

  $(document).ready( () => {
    // Set form state on load and on input to notice_class field
    setFormState($('#id_notice_class').val());
    $('#id_notice_class').on('input', (e) => {
      setFormState(e.target.value);
    });
  });
})(django.jQuery);
