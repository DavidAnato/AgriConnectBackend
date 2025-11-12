from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

User = get_user_model()

class LoginResponseTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="test@example.com",
            password="testpassword123",
            first_name="Test",
            last_name="User",
            role="producer",
            phone_number="+1234567890",
            farm_name="Test Farm",
            farm_address="123 Farm Street",
            farm_description="A test farm"
        )
        self.user.verified_email = True
        self.user.save()

    def test_login_response_includes_all_user_data(self):
        """Test that login response includes all important user information"""
        response = self.client.post('/authentication/login/', {
            'email': 'test@example.com',
            'password': 'testpassword123'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check that all important user data is included
        user_data = response.data['user']
        
        # Essential fields
        self.assertIn('id', user_data)
        self.assertIn('email', user_data)
        self.assertIn('first_name', user_data)
        self.assertIn('last_name', user_data)
        self.assertIn('role', user_data)
        self.assertIn('verified_email', user_data)
        
        # Additional important fields for frontend storage
        self.assertIn('phone_number', user_data)
        self.assertIn('is_active', user_data)
        self.assertIn('is_staff', user_data)
        self.assertIn('farm_name', user_data)
        self.assertIn('farm_address', user_data)
        self.assertIn('farm_description', user_data)
        self.assertIn('google_id', user_data)
        self.assertIn('profile_picture', user_data)
        self.assertIn('date_joined', user_data)
        
        # Verify values
        self.assertEqual(user_data['email'], 'test@example.com')
        self.assertEqual(user_data['first_name'], 'Test')
        self.assertEqual(user_data['last_name'], 'User')
        self.assertEqual(user_data['role'], 'producer')
        self.assertEqual(user_data['phone_number'], '+1234567890')
        self.assertEqual(user_data['farm_name'], 'Test Farm')
        self.assertEqual(user_data['farm_address'], '123 Farm Street')
        self.assertEqual(user_data['farm_description'], 'A test farm')
        self.assertTrue(user_data['is_active'])
        self.assertFalse(user_data['is_staff'])
