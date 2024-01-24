(function($) {
  const setFormState = (notice_class) => {
    const formFields = $('[class*="field-"]').not('.field-notice_class');
    const warning = $(
      `<p id="image-class-warning" style="font-size: 1.2rem; color: firebrick; background: lightsalmon; padding: .25rem 1rem; border-radius: .5rem;">
        Warning: This notice class is deprecated.
        Please use the "Image" notice class instead.
      </p>`
    );
    if (notice_class === 'none') {
      // Image class - warn deprecated
      $('.field-notice_class .help').append(warning);
      formFields.hide()
    } else {
      $('#image-class-warning').remove();
      formFields.show()
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
