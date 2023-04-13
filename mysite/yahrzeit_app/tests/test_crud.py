"""Unit tests for CRUD module."""

from django.test import TestCase
from .. import crud
from ..models import CustomUser, Decedent


class CRUDUserTestCase(TestCase):
    """Tests for User-oriented CRUD functions."""

    def setUp(self):
        """Set-up to happen before each test.

        Create a test user for use with functions that depend on an existing
        user.

        """

        CustomUser.objects.create_user(
            email='test1@test.test',
            password='testpassword',
        )

    def test_create_user(self):
        """Test the create_user function.

        Verify that the successful creation of a user returns True, that the
        new record contains the correct email, and that an attempt to create
        another user whth the same email returns False.

        """

        self.assertTrue(
            crud.create_user(
                'test2@test.test',
                'testpassword',
            ),
            'The creation of a new user with a unique email should return True',
        )
        test_user = CustomUser.objects.get(pk=2)
        self.assertEqual(
            test_user.email,
            'test2@test.test',
            'The new user (id 2) should have the email \'test2@test.test\'',
        )

        self.assertFalse(
            crud.create_user(
                'test2@test.test',
                'testpassword',
            ),
            'create_user should return False because that email is taken',
        )

    def test_get_user_by_email(self):
        """Test the get_user_by_email function.

        Check that when a given email is passed into the function, the user
        with the same email is returned. Verify that a query for an email not
        associated with a user returns None.

        """

        self.assertEqual(
            crud.get_user_by_email('test1@test.test').email,
            'test1@test.test',
            'Email of returned user should match the email argument',
        )

        self.assertIsNone(
            crud.get_user_by_email(
                'test2@test.test',
            ),
            'Query for a nonexistant user should return None',
        )


class CRUDDecedentTestCase(TestCase):
    """Tests for Decedent-oriented CRUD functions."""

    def setUp(self):
        """Set-up to happen before each test.

        Create test users and decedents for use in functions that depend
        on preexisting records.

        """

        self.test_user1 = CustomUser.objects.create_user(
            email='test1@test.test',
            password='testpassword',
        )
        self.test_user2 = CustomUser.objects.create_user(
            email='test2@test.test',
            password='testpassword',
        )
        self.test_user3 = CustomUser.objects.create_user(
            email='test3@test.test',
            password='testpassword',
        )

        Decedent.objects.create(
            user=self.test_user1,
            name='TestDecedent1',
            death_date_hebrew='5783-10-11',
            next_date_hebrew='5784-10-11',
            next_date_gregorian='2023-12-23',
        )
        Decedent.objects.create(
            user=self.test_user1,
            name='TestDecedent2',
            death_date_hebrew='5779-03-22',
            next_date_hebrew='5783-03-22',
            next_date_gregorian='2023-06-11',
        )
        Decedent.objects.create(
            user=self.test_user1,
            name='TestDecedent3',
            death_date_hebrew='5778-08-28',
            next_date_hebrew='5784-08-28',
            next_date_gregorian='2023-11-12',
        )
        Decedent.objects.create(
            user=self.test_user2,
            name='TestDecedent4',
            death_date_hebrew='5783-11-16',
            next_date_hebrew='5784-11-16',
            next_date_gregorian='2024-01-26',
        )
        Decedent.objects.create(
            user=self.test_user2,
            name='TestDecedent5',
            death_date_hebrew='5781-02-21',
            next_date_hebrew='5782-02-21',
            next_date_gregorian='2022-05-22',
        )
        Decedent.objects.create(
            user=self.test_user2,
            name='TestDecedent6',
            death_date_hebrew='5780-10-20',
            next_date_hebrew='5781-10-20',
            next_date_gregorian='2021-01-04',
        )

    def test_create_decedent(self):
        """Test the create_decedent function.

        Verify that this function creates a decedent record that maintains the
        correct values for death_date_hebrew, next_date_hebrew, and
        next_date_gregorian.

        """

        self.assertIsNone(
            crud.create_decedent(
                CustomUser.objects.get(pk=1),
                'TestDecedent7',
                '5783-12-09',
                '5784-12-09',
                '2024-02-18',
            ),
            'create_decedent should return None',
        )

        test_decedent = Decedent.objects.filter(name='TestDecedent7').first()
        self.assertEqual(
            test_decedent.death_date_hebrew,
            '5783-12-09',
            'death_date_hebrew should equal corresponding argument',
        )
        self.assertEqual(
            test_decedent.next_date_hebrew,
            '5784-12-09',
            'next_date_hebrew should equal corresponding argument',
        )
        self.assertEqual(
            test_decedent.next_date_gregorian,
            '2024-02-18',
            'next_date_gregorian should equal corresponding argument',
        )

    def test_get_decedents_for_user(self):
        """Test the get_decedents_for_user function.

        Check that the QuerySet returned by the function when it is called
        on user 1 has a length of 3 and that the names for the three decedents
        match those of the decedents instantiated in setUp. Verify that the
        QuerySet returned for a nonexistant user and the QuerySet returned for
        a user with no decedents have lengths of 0.

        """

        user1_decedents = crud.get_decedents_for_user(self.test_user1)
        self.assertEqual(
            len(user1_decedents),
            3,
            'User 1 should have three decedents',
        )

        self.assertEqual(
            set(user1_decedents.keys()),
            {
                'TestDecedent1',
                'TestDecedent2',
                'TestDecedent3',
            },
            'Decedent names should match TestDecedent(1,2,3)',
        )

        # self.assertEqual(
        #     len(crud.get_decedents_for_user(4)),
        #     0,
        #     'A nonexistant user should have no decedents',
        # )
        self.assertEqual(
            len(crud.get_decedents_for_user(self.test_user3)),
            0,
            'User 3 should have no decedents',
        )

    def test_update_decedents_for_user(self):
        """Test the update_decedents_for_user function.

        Verify that calling this function on user 2

        """

        crud.update_decedents_for_user(CustomUser.objects.get(pk=2))
        self.assertEqual(
            Decedent.objects.get(name='TestDecedent5').next_date_hebrew,
            '5783-02-21',
            'TestDecedent5\'s next_date_hebrew should update to 5783-02-21',
        )
        self.assertEqual(
            Decedent.objects.get(name='TestDecedent5').next_date_gregorian,
            '2023-05-12',
            'TestDecedent5\'s next_date_gregorian should update to 2023-05-12',
        )
        self.assertEqual(
            Decedent.objects.get(name='TestDecedent6').next_date_hebrew,
            '5784-10-20',
            'TestDecedent6\'s next_date_hebrew should update to 5784-10-20',
        )
        self.assertEqual(
            Decedent.objects.get(name='TestDecedent6').next_date_gregorian,
            '2024-01-01',
            'TestDecedent6\'s next_date_gregorian should update to 2024-01-01',
        )
