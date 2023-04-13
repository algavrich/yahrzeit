"""Unit tests for views module."""

from datetime import date
from django.test import TestCase, Client
from django.http import HttpResponse, JsonResponse
from ..helpers import js_key
from ..models import CustomUser, Decedent


c = Client()


class IndexTestCase(TestCase):
    """Tests for index view function."""

    def setUp(self):
        """Set-up to happen before each test.

        Create a test user for testing functionality that depends on whether
        there is a user logged in.

        """

        CustomUser.objects.create_user(
            email='test@test.test',
            password='testpassword',
        )

    def test_index(self):
        """Test the index view function.

        Make a request to the index and verify that the subsequent response is
        of the type HttpResponse and has the proper content.

        Make an additional request to the index as a logged-in user, and
        verify again that the type and content of the response are appropriate
        for the given context.

        """

        idx_response = c.get('/yahrzeit/')
        self.assertIsInstance(idx_response, HttpResponse)
        self.assertContains(idx_response, '<h4>Date of Death</h4>')
        self.assertContains(idx_response, 'Login')
        self.assertContains(
            idx_response,
            f'max=\"{date.strftime(date.today(), "%Y-%m-%d")}\"',
        )

        c.login(email='test@test.test', password='testpassword')
        logged_in_idx_response = c.get('/yahrzeit/')
        self.assertIsInstance(logged_in_idx_response, HttpResponse)
        self.assertContains(logged_in_idx_response, 'Dashboard')


class CreateAccountTestCase(TestCase):
    """Tests for views pertaining to creating an account."""

    def setUp(self):
        """Set-up to happen before each test.

        Create a test user for testing functionality that depends on whether
        there is a user logged in.

        """

        CustomUser.objects.create_user(
            email='test1@test.test',
            password='testpassword',
        )

    def test_create_account_form(self):
        """Test the create_account_form view function.

        Make a request to create_account_form and verify that the subsequent
        response is of the type HttpResponse and has the proper content.

        Make an additional request to create_account_form as a logged-in user,
        and verify that the response redirects to the dashboard.

        """

        caf_response = c.get('/yahrzeit/create-account-form')
        self.assertIsInstance(caf_response, HttpResponse)
        self.assertContains(caf_response, '<h2>Create Account</h2>')

        c.login(email='test1@test.test', password='testpassword')
        logged_in_caf_response = c.get(
            '/yahrzeit/create-account-form',
            follow=True,
        )
        self.assertRedirects(logged_in_caf_response, '/yahrzeit/dashboard')

    def test_do_create_account(self):
        """Test the do_create_account view function.

        Make a valid POST request to do_create_account and verify that it is
        of the type JsonResponse, has a status of success, and results in the
        new user being logged in.

        Make an additional, invalid (email already taken) POST request to
        do_create_account, and verify that a JsonResponse with status failure
        is returned and that no user is logged in.

        """

        create_account_response = c.post(
            '/yahrzeit/api/create-account',
            {'email': 'test2@test.test', 'password': 'testpassword'},
            content_type='application/json',
        )
        self.assertIsInstance(create_account_response, JsonResponse)
        self.assertEqual(create_account_response.json()['status'], 'success')
        self.assertEqual(c.session['_auth_user_id'], '2')

        c.logout()
        create_account_response2 = c.post(
            '/yahrzeit/api/create-account',
            {'email': 'test2@test.test', 'password': 'testpassword'},
            content_type='application/json',
        )
        self.assertIsInstance(create_account_response2, JsonResponse)
        self.assertEqual(create_account_response2.json()['status'], 'failure')
        self.assertNotIn('_auth_user_id', c.session)


class LoginTestCase(TestCase):
    """Tests for view functions pertaining to logging in."""

    def setUp(self):
        """Set-up to happen before each test.

        Create a test user for testing functionality that depends on whether
        there is a user logged in.

        """

        CustomUser.objects.create_user(
            email='test1@test.test',
            password='testpassword',
        )

    def test_login_form(self):
        """Test the login_form view function.

        Make a request to login_form and verify that the subsequent
        response is of the type HttpResponse and has the proper content.

        Make an additional request to login_form as a logged-in user,
        and verify that the response redirects to the dashboard.

        """

        login_form_response = c.get('/yahrzeit/login-form')
        self.assertIsInstance(login_form_response, HttpResponse)
        self.assertContains(login_form_response, '<h2>Login</h2>')

        c.login(email='test1@test.test', password='testpassword')
        logged_in_login_form_response = c.get(
            '/yahrzeit/login-form',
            follow=True,
        )
        self.assertRedirects(
            logged_in_login_form_response,
            '/yahrzeit/dashboard',
        )

    def test_do_login(self):
        """Test the do_login view function.

        Make a POST request to do_login  for an existing user and verify that
        the subsequent response successfully logs the user in and redirects to
        their dashboard.

        Make an additional POST request to do_login as a nonexistant user,
        and verify that the response redirects to the login form and does not
        log any user in.

        """

        login_response = c.post(
            '/yahrzeit/login',
            {'email': 'test1@test.test', 'password': 'testpassword'},
            follow=True,
        )
        self.assertRedirects(login_response, '/yahrzeit/dashboard')
        self.assertEqual(c.session['_auth_user_id'], '1')

        c.logout()
        wrong_email_login_response = c.post(
            '/yahrzeit/login',
            {'email': 'test2@test.test', 'password': 'bestbassword'},
            follow=True,
        )
        self.assertRedirects(
            wrong_email_login_response,
            '/yahrzeit/login-form',
        )
        self.assertNotIn('auth_user_id', c.session)

    def test_do_logout(self):
        """Test the do_logout view function.

        Make a request to do_logout as a logged in user and verify that the
        subsequent response redirects to the index and actually logs the user
        out.

        """

        c.login(email='test1@test.test', password='testpassword')
        logout_response = c.get('/yahrzeit/logout', follow=True)
        self.assertRedirects(logout_response, '/yahrzeit/')
        self.assertNotIn('_auth_user_id', c.session)


class DashboardTestCase(TestCase):
    """Test for the dashboard view function."""

    def setUp(self):
        """Set-up to happen before each test.

        Create a test user for testing functionality that depends on whether
        there is a user logged in.

        Additionally, create a test decedent for testing that a user's
        decedent data is correctly displayed on the dashboard.

        """

        self.test_user = CustomUser.objects.create_user(
            email='test@test.test',
            password='testpassword',
        )
        self.new_dec = Decedent.objects.create(
            user=self.test_user,
            name='testdecedent',
            death_date_hebrew='5782-11-30',
            next_date_hebrew='5784-11-30',
            next_date_gregorian='2024-02-09',
        )

    def test_dashboard(self):
        """Test the dashboard view function.

        Make a request to dashboard as an anonymous user and verify that the
        subsequent response redirects to the login form.

        Make an additional request to dashboard as a logged-in user,
        and verify that the response is an HttpResponse with the appropriate
        content, including decedent data.

        """

        anon_user_dash_response = c.get('/yahrzeit/dashboard', follow=True)
        self.assertRedirects(
            anon_user_dash_response,
            '/yahrzeit/login-form?next=/yahrzeit/dashboard',
        )

        c.login(email='test@test.test', password='testpassword')
        dash_response = c.get('/yahrzeit/dashboard')
        self.assertIsInstance(dash_response, HttpResponse)
        self.assertContains(dash_response, '<h2>Your Dashboard</h2>')
        self.assertContains(
            dash_response,
            'testdecedent\'s next yahrzeit is 30 Shevat 5784 / 9 February 2024',
        )


class CalculateTestCase(TestCase):
    def setUp(self):
        pass

    def test_calculate(self):
        anon_user_calc_response = c.post(
            '/yahrzeit/calculate',
            {
                'decedent-name': 'testdecedent',
                'decedent-date': '2022-02-01',
                'TOD': 'before-sunset',
                'number': '1',
            },
        )
        self.assertIsInstance(anon_user_calc_response, HttpResponse)
        self.assertContains(
            anon_user_calc_response,
            'testdecedent\'s next yahrzeit is 30 Shevat 5784 which is 9 February 2024',
        )
