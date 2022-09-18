"""For validating submitted form data."""

import logging
from django.core.exceptions import ValidationError
from utils.institution import is_institution_email

logger = logging.getLogger('django')


def institutional_email(email):
    """Raise an error if the email is not from a recognised institute."""
    if not is_institution_email(email):
        logger.info(f"Not a recognised institutional email: {email}")
        raise ValidationError(
            (
                'Sorry, this is not a recognised Australian institute'
                ' email address.'
            ),
            code="invalid_email",
        )
