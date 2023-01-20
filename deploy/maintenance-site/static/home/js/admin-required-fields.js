// Mark required and optional fields in admin forms

const TAGS = ['input', 'textarea'];

($ => {
  $(document).ready( () => {
    // Create a 'required' label to place beneath fields
    const label = $('<small style="color: #ffb042; line-height: 3;"><em>Required</em></small>')

    TAGS.forEach( (tag) => {
      // Append label to required elements for each tag
      $(`${tag}[required]`).after(label.clone()[0]);
      $(`${tag}[required]`).after($('<br>')[0]);
    })
  });
})(django.jQuery);
