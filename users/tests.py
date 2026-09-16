from django.contrib.auth.models import User
from django.core import mail
from django.test import Client, TestCase, override_settings
from django.urls import reverse
import re


class RoleRegistrationRulesTest(TestCase):
    def test_public_registration_accepts_customer_role(self):
        client = Client()
        payload = {
            'username': 'customer01',
            'email': 'customer01@example.com',
            'password': 'password123',
            'firstName': 'Test',
            'lastName': 'Customer',
            'role': 'CUSTOMER',
        }
        response = client.post('/api/users/register/', payload, content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertTrue(User.objects.filter(username='customer01').exists())

    def test_public_registration_rejects_admin_operator_courier(self):
        client = Client()
        for forbidden_role in ('ADMIN', 'OPERATOR', 'COURIER'):
            payload = {
                'username': f'{forbidden_role.lower()}01',
                'email': f'{forbidden_role.lower()}01@example.com',
                'password': 'password123',
                'firstName': 'Role',
                'lastName': forbidden_role,
                'role': forbidden_role,
            }
            response = client.post('/api/users/register/', payload, content_type='application/json')
            self.assertEqual(response.status_code, 400)


@override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
class PasswordResetFlowTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='old-name',
            email='reset@example.com',
            password='old-password123',
        )
        self.client = Client()

    def test_password_reset_verifies_code_and_updates_credentials(self):
        response = self.client.post(
            reverse('password-reset-request'),
            {'email': 'reset@example.com'},
            content_type='application/json',
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        code = re.search(r'\b\d{6}\b', mail.outbox[0].body).group()

        invalid_response = self.client.post(
            reverse('password-reset-verify'),
            {'email': 'reset@example.com', 'code': '000000'},
            content_type='application/json',
        )
        self.assertEqual(invalid_response.status_code, 400)

        verify_response = self.client.post(
            reverse('password-reset-verify'),
            {'email': 'reset@example.com', 'code': code},
            content_type='application/json',
        )
        self.assertEqual(verify_response.status_code, 200)
        reset_token = verify_response.json()['resetToken']

        reset_response = self.client.post(
            reverse('password-reset'),
            {
                'resetToken': reset_token,
                'username': 'new-name',
                'password': 'new-password123',
            },
            content_type='application/json',
        )
        self.assertEqual(reset_response.status_code, 200)
        self.assertTrue(self.client.login(username='new-name', password='new-password123'))

        reused_token_response = self.client.post(
            reverse('password-reset'),
            {
                'resetToken': reset_token,
                'username': 'another-name',
                'password': 'another-password123',
            },
            content_type='application/json',
        )
        self.assertEqual(reused_token_response.status_code, 400)
