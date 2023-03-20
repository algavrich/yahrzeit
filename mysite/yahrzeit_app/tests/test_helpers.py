"""Unit tests for helpers module."""

from unittest import skip
from datetime import date
from django.test import TestCase
from pyluach import dates
from .. import helpers
from ..models import User


class StringConversionsTestCase(TestCase):
    """Tests for various string conversion functions."""

    def test_date_from_string(self):
        """Test the date_from_string function.

        Verify that the function returns a date object

        """
        self.assertEqual(
            helpers.date_from_string('2023-03-11'),
            date(2023, 3, 11),
            'Date was not parsed correctly',
        )

    def test_greg_to_heb(self):
        self.assertEqual(
            helpers.greg_to_heb('2023-03-11'),
            '5783-12-18',
            'Date did not translate correctly',
        )

    def test_h_date_stringify_res(self):
        self.assertEqual(
            helpers.h_date_stringify_res(
                dates.HebrewDate(5783, 12, 18)
            ),
            '18 Adar 5783',
            'Date string should equal \'18 Adar 5783\'',
        )

    def test_h_date_stringify_db(self):
        self.assertEqual(
            helpers.h_date_stringify_db(
                dates.HebrewDate(5783, 12, 18)
            ),
            '5783-12-18',
            'Date string should equal \'5783-12-18\'',
        )

    def test_g_date_stringify_res(self):
        self.assertEqual(
            helpers.g_date_stringify_res(
                dates.GregorianDate(2023, 3, 11)
            ),
            '11 March 2023',
            'Date string should equal \'11 March 2023\'',
        )

    def test_g_date_stringify_db(self):
        self.assertEqual(
            helpers.g_date_stringify_db(
                dates.GregorianDate(2023, 3, 11)
            ),
            '2023-03-11',
            'Date string should equal \'2023-03-11\'',
        )


class FutureDatesTestCase(TestCase):
    """Test for functions that calculate future yahrzeits."""

    def test_get_next_date(self):
        self.assertEqual(
            helpers.get_next_date('2023-02-01', False),
            (
                dates.HebrewDate(5784, 11, 10),
                dates.GregorianDate(2024, 1, 20),
                dates.GregorianDate(2024, 1, 20).to_pydate() == date.today(),
            ),
            'Incorrect yahrzeit calculation',
        )
        self.assertEqual(
            helpers.get_next_date('2023-02-01', True),
            (
                dates.HebrewDate(5784, 11, 11),
                dates.GregorianDate(2024, 1, 21),
                dates.GregorianDate(2024, 1, 21).to_pydate() == date.today(),
            ),
            'Incorrect yahrzeit calculation',
        )

    def test_get_following_dates(self):
        self.assertEqual(
            helpers.get_following_dates(dates.HebrewDate(5784, 11, 11), 5),
            {
                '11 Shevat 5785': '9 February 2025',
                '11 Shevat 5786': '29 January 2026',
                '11 Shevat 5787': '19 January 2027',
                '11 Shevat 5788': '8 February 2028',
                '11 Shevat 5789': '27 January 2029',
            },
            'Future dates did not calculate correctly',
        )


@skip('Reduce api calls')
class SunsetTimeTestCase(TestCase):
    """Test for function that calculates sunset time."""

    def test_get_sunset_time(self):
        self.assertEqual(
            helpers.get_sunset_time(
                '2023-03-15',
                '1517 Fountain St, Alameda, CA 94501, USA',
            ),
            '7:15 PM',
            'Sunset time incorrect',
        )
        self.assertEqual(
            helpers.get_sunset_time(
                '2022-12-29',
                'Norway, 3814 Tromsø, Norway',
            ),
            None,
            'There should be no sunset for this place and date',
        )


class PasswordHashingTestCase(TestCase):
    """Tests for password hashing functions."""

    def setUp(self):
        self.test_user = User(
            email='test@test.test',
            password=helpers.hash_password('Password1!'),
        )

    def test_hash_password(self):
        self.assertEqual(len(self.test_user.password), 97)
        self.assertEqual(
            self.test_user.password[:31],
            '$argon2id$v=19$m=65536,t=3,p=4$',
            'Hash does not have the correct prefix',
        )

    def test_verify_password(self):
        self.assertTrue(
            helpers.verify_password(
                self.test_user,
                'Password1!',
            )
        )
        self.assertFalse(
            helpers.verify_password(
                self.test_user,
                'opihanwlrg',
            )
        )
