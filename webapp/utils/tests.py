"""Test utilities."""

from django.test import TestCase
from .institution import is_institution_email


class InstitutionEmailTestCase(TestCase):
    def test_valid_institution_email(self):
        email = "john.doe@uq.edu.au"
        self.assertTrue(is_institution_email(email))

    def test_invalid_institution_email(self):
        email = "john.doe@gmail.com"
        self.assertFalse(is_institution_email(email))

    def test_missing_at_symbol(self):
        email = "john.doe"
        with self.assertRaises(ValueError):
            is_institution_email(email)

    def test_wildcard_domain_match(self):
        email = "john.doe@subdomain.uq.edu.au"
        self.assertTrue(is_institution_email(email))
