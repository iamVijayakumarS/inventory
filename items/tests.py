from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from .models import Inventory_Items


User = get_user_model()

class ItemCreateViewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123")
        self.token = str(AccessToken.for_user(self.user))

    def test_create_item(self):
        url = reverse('item-create')
        data = {
            "name": "Test Item",
            "description": "Test Item Description"
        }
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Item created successfully')

    def test_create_item_fail_without_authentication(self):
        url = reverse('item-create')
        data = {
            "name": "Test Item",
            "description": "Test Item Description"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ItemDetailViewOrUpdateOrDeleteTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword123")
        self.token = str(AccessToken.for_user(self.user))
        self.item = Inventory_Items.objects.create(
            name="Test Item", description="Test Item Description"
        )

    def test_get_item(self):
        url = reverse('item-read', kwargs={'item_id': self.item.id})
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_update_item(self):
        url = reverse('item-read', kwargs={'item_id': self.item.id})
        data = {
            "name": "Updated Item",
            "description": "Updated Description"
        }
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], 'Updated Item')

    def test_delete_item(self):
        url = reverse('item-read', kwargs={'item_id': self.item.id})
        # Authenticate the user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_item_fail_without_authentication(self):
        url = reverse('item-read', kwargs={'item_id': self.item.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
