// Check whether a user's email is associated with an Australian institution

$(document).ready( function() {

  const DEBOUNCE_MS = 1000;
  const input = $('#emailValidInput');
  const loadingIcon = $('#emailValidLoading');
  const resultText = $('#emailValidResult');
  const validMessageHtml = `
    Great news! Your email address is associated with
    an institution on our list.`;
  const invalidMessageHtml = `
    Sorry, this email address is not associated with an institution on our list.
    <br>
    Please
    <a href="/request/support">contact us</a>
    if you would like to discuss the addition of your institution to our list.`;

  function resetValidateEmail() {
    loadingIcon.hide();
    input.removeClass('is-valid');
    input.removeClass('is-invalid');
    resultText.empty();
    resultText.removeClass('text-danger');
    resultText.removeClass('text-success');
  }

  function fetchValidateEmail() {
    const email = $(this).val();
    if (email.length > 0) {
      loadingIcon.show();
      $.ajax({
        url: '/institution/validate',
        type: 'GET',
        data: {
          email: email
        },
        success: function(data) {
          loadingIcon.hide();
          if (data.valid) {
            input.addClass('is-valid');
            input.removeClass('is-invalid');
            resultText.html(validMessageHtml);
            resultText.removeClass('text-danger');
            resultText.addClass('text-success');
            return;
          }
          if (data.valid === false) {
            input.addClass('is-invalid');
            input.removeClass('is-valid');
            resultText.html(invalidMessageHtml);
            resultText.removeClass('text-success');
            resultText.addClass('text-danger');
            return;
          }
          if (data.error) {
            input.addClass('is-invalid');
            input.removeClass('is-valid');
            resultText.html(data.error);
            resultText.removeClass('text-success');
            resultText.addClass('text-danger');
            return;
          }
          // If not data.valid in response, do nothing
          resetValidateEmail();
        }
      });
    } else {
      resetValidateEmail();
    }
  }

  $('input').on('input', _.debounce(
    fetchValidateEmail,
    DEBOUNCE_MS,
    { 'leading': false, 'trailing': true },
  ));
});
