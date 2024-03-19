"""Test utilities."""

from django.test import TestCase
from unittest import mock
from . import institution
from .institution import is_institution_email


MOCK_DOMAIN_LIST = {
    "*.gov.au": "Any Australian Government Funded Research Organisation",
    "@uni.edu.au": "The University of Queensland",
    "@students.uni.edu.au": "The University of Queensland",
}


class InstitutionEmailTestCase(TestCase):

    def setUp(self):
        self.domain_list = mock.patch.object(
            institution,
            "get_domains",
            return_value=MOCK_DOMAIN_LIST)

    def test_valid_institution_email(self):
        email = "john.doe@uni.edu.au"
        with self.domain_list:
            self.assertTrue(is_institution_email(email))

    def test_invalid_institution_email(self):
        email = "john.doe@gmail.com"
        with self.domain_list:
            self.assertFalse(is_institution_email(email))

    def test_missing_at_symbol(self):
        email = "john.doe"
        with self.assertRaises(ValueError):
            with self.domain_list:
                is_institution_email(email)

    def test_subdomain_match(self):
        email = "john.doe@students.uni.edu.au"
        with self.domain_list:
            self.assertTrue(is_institution_email(email))

    def test_implicit_wildcard_subdomain_match(self):
        email = "john.doe@subdomain.uni.edu.au"
        with self.domain_list:
            self.assertTrue(is_institution_email(email))

    def test_explicit_wildcard_subdomain_match(self):
        email = "john.doe@subdomain.gov.au"
        with self.domain_list:
            self.assertTrue(is_institution_email(email))
