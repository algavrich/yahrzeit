"""Unit tests for views module."""

from unittest import skip
from django.test import TestCase, Client
from .. import views
from ..models import User
from argon2 import PasswordHasher


c = Client()
ph = PasswordHasher()


class IndexTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            email='test@test.test',
            password=ph.hash('Password1!'),
        )

    def test_index(self):
        idx_response = c.get('/yahrzeit/')
        self.assertContains(idx_response, 'Date of Death')
        self.assertContains(idx_response, 'Login')
        session = c.session
        session['user_id'] = self.test_user.pk
        session.save()
        logged_in_idx_response = c.get('/yahrzeit/')
        self.assertContains(logged_in_idx_response, 'Dashboard')

    def tearDown(self):
        session = c.session
        session.pop('user_id')
        session.save()


class CreateAccountTestCase(TestCase):
    def setUp(self):
        self.test_user = User.objects.create(
            email='test@test.test',
            password=ph.hash('Password1!'),
        )

    def test_create_account_form(self):
        caf_response = c.get('/yahrzeit/create-account-form')
        self.assertContains(caf_response, 'Create Account')
        session = c.session
        session['user_id'] = self.test_user.pk
        session.save()
        logged_in_caf_response = c.get(
            '/yahrzeit/create-account-form', follow=True)
        self.assertContains(logged_in_caf_response, 'Dashboard')

    def tearDown(self):
        session = c.session
        session.pop('user_id')
        session.save()
