from django.contrib.auth.models import User
from django.test import Client, TestCase


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
