"""Test utilities."""

import os
import shutil
import time
from unittest import mock

import requests
import requests_mock
from django.test import TestCase

from . import institution
from .institution import is_institution_email
from .test.data import TEST_APPROVED_DOMAINS


MOCK_DOMAIN_LIST = {
    "*.gov.au": "Any Australian Government Funded Research Organisation",
    "@uni.edu.au": "The University of Queensland",
    "@students.uni.edu.au": "The University of Queensland",
}


class InstitutionEmailTestCase(TestCase):

    def setUp(self):
        self.domain_list = mock.patch.object(
            institution,
            "get_email_domains",
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


class ApprovedDomainsCacheTestCase(TestCase):
    """Test fetching and caching of the remote approved domains list."""

    def setUp(self):
        shutil.rmtree(institution.CACHE_DIR, ignore_errors=True)

    def tearDown(self):
        shutil.rmtree(institution.CACHE_DIR, ignore_errors=True)

    def test_institutions_are_sorted_with_bare_domains(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL,
                  json=TEST_APPROVED_DOMAINS)
            institutions = institution.get_institutions()
        self.assertEqual(
            [i['name'] for i in institutions],
            [
                "Australian Genome Research Facility",
                "Australian Government",
                "The University of Queensland",
            ],
        )
        self.assertEqual(institutions[1]['domains'], ["*.gov.au"])
        self.assertEqual(
            institutions[2]['domains'],
            ["uq.edu.au", "student.uq.edu.au"],
        )

    def test_email_domains_are_prefixed(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL,
                  json=TEST_APPROVED_DOMAINS)
            domains = institution.get_email_domains()
        self.assertEqual(domains["@uq.edu.au"], "The University of Queensland")
        self.assertIn("*.gov.au", domains)
        self.assertNotIn("uq.edu.au", domains)

    def test_is_institution_email_uses_remote_list(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL,
                  json=TEST_APPROVED_DOMAINS)
            self.assertTrue(is_institution_email("a@uq.edu.au"))
            self.assertTrue(is_institution_email("a@x.uq.edu.au"))
            self.assertTrue(is_institution_email("a@health.gov.au"))
            self.assertFalse(is_institution_email("a@gmail.com"))

    def test_cache_hit_does_not_refetch(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL,
                  json=TEST_APPROVED_DOMAINS)
            institution.get_institutions()
            institution.get_email_domains()
            institution.get_institutions()
            self.assertEqual(m.call_count, 1)

    def test_expired_cache_refetches(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL,
                  json=TEST_APPROVED_DOMAINS)
            institution.get_institutions()
            expired = time.time() - institution.CACHE_SECONDS - 60
            for path in (
                institution.INSTITUTIONS_CACHE_PATH,
                institution.DOMAINS_CACHE_PATH,
            ):
                os.utime(path, (expired, expired))
            institution.get_institutions()
            self.assertEqual(m.call_count, 2)

    def test_fetch_failure_serves_stale_cache(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL,
                  json=TEST_APPROVED_DOMAINS)
            institution.get_institutions()
            expired = time.time() - institution.CACHE_SECONDS - 60
            os.utime(institution.INSTITUTIONS_CACHE_PATH, (expired, expired))
            m.get(institution.APPROVED_DOMAINS_URL, status_code=500)
            institutions = institution.get_institutions()
        self.assertEqual(len(institutions), 3)

    def test_fetch_failure_without_cache_raises(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL, status_code=500)
            with self.assertRaises(requests.HTTPError):
                institution.get_institutions()

    def test_fetch_failure_defers_retry(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL,
                  json=TEST_APPROVED_DOMAINS)
            institution.get_institutions()
            self._expire_cache()
            m.get(institution.APPROVED_DOMAINS_URL, status_code=500)
            institution.get_institutions()
            institution.get_institutions()
            institution.get_email_domains()
            # 1 initial fetch + 1 failed retry; cooldown blocks the rest
            self.assertEqual(m.call_count, 2)

            # Retry happens again once the cooldown has passed
            self._expire_cache()
            institution.get_institutions()
            self.assertEqual(m.call_count, 3)

    def test_write_leaves_no_temp_files(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL,
                  json=TEST_APPROVED_DOMAINS)
            institution.get_institutions()
        self.assertEqual(
            sorted(p.name for p in institution.CACHE_DIR.iterdir()),
            ['domains.json', 'institutions.json'],
        )

    def test_write_failure_cleans_temp_file(self):
        with requests_mock.Mocker() as m:
            m.get(institution.APPROVED_DOMAINS_URL,
                  json=TEST_APPROVED_DOMAINS)
            with mock.patch.object(
                institution.os,
                'replace',
                side_effect=OSError('disk error'),
            ):
                with self.assertRaises(OSError):
                    institution.get_institutions()
        self.assertEqual(list(institution.CACHE_DIR.iterdir()), [])

    def _expire_cache(self):
        expired = time.time() - institution.CACHE_SECONDS - 60
        for path in (
            institution.INSTITUTIONS_CACHE_PATH,
            institution.DOMAINS_CACHE_PATH,
        ):
            os.utime(path, (expired, expired))
