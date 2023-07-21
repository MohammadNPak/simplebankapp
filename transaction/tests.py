from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.test import TestCase
from .models import Transaction,Category
from rest_framework.test import APITestCase

class CategoryAPITestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser', password='testpassword')
        
        self.admin_user = User.objects.create_superuser(
            username='adminuser', password='adminpassword')

    def get_user_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_list_categories(self):
        # Create test categories
        category1 = Category.objects.create(name='Category 1')
        category2 = Category.objects.create(name='Category 2')

        url = '/api/categories/'
        token = self.get_user_jwt_token(self.user)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        api_categories = response.data
        # Get the actual categories from the database
        actual_categories = Category.objects.all()
        # Compare the API response data with the actual categories in the database
        self.assertEqual(len(api_categories), actual_categories.count())

        for api_category, actual_category in zip(api_categories, actual_categories):
            self.assertEqual(api_category['id'], actual_category.id)
            self.assertEqual(api_category['name'], actual_category.name)


    def test_create_category_as_admin(self):
        url = '/api/categories/'
        data = {'name': 'New Category'}

        token = self.get_user_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)
        category = Category.objects.first()
        self.assertEqual(category.name, response.data['name'])
        self.assertEqual(category.id, response.data['id'])

    def test_create_category_as_regular_user(self):
        url = '/api/categories/'
        data = {'name': 'New Category'}

        token = self.get_user_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 0)

    def test_update_category_as_admin(self):
        # Create a test category
        category = Category.objects.create(name='Category 1')

        url = f'/api/categories/{category.id}/'
        data = {'name': 'Updated Category'}

        token = self.get_user_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        category.refresh_from_db()
        self.assertEqual(category.name, 'Updated Category')

    def test_update_category_as_regular_user(self):
        # Create a test category
        category = Category.objects.create(name='Category 1')

        url = f'/api/categories/{category.id}/'
        data = {'name': 'Updated Category'}

        token = self.get_user_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.put(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        category.refresh_from_db()
        self.assertNotEqual(category.name, 'Updated Category')

    def test_delete_category_as_admin(self):
        # Create a test category
        category = Category.objects.create(name='Category 1')

        url = f'/api/categories/{category.id}/'

        token = self.get_user_jwt_token(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), 0)

    def test_delete_category_as_regular_user(self):
        # Create a test category
        category = Category.objects.create(name='Category 1')

        url = f'/api/categories/{category.id}/'

        token = self.get_user_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Category.objects.count(), 1)



class TransactionAPITestCase1(APITestCase):
    def setUp(self):
        # Create test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create test category
        self.category = Category.objects.create(name='Category1')

        # Generate JWT token for the test user
        self.token = self.get_user_jwt_token(self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    def get_user_jwt_token(self, user):
        # Generate JWT token for the user
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    # def create_test_transaction(self):
    #     transaction_data = {
    #         'Amount': '100.00',
    #         'Type': 'I',
    #         'Category': str(self.category),
    #     }

    #     response = self.client.post('/api/transactions/', transaction_data, format='json')
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    #     return response.data

    def test_create_transaction(self):
        initial_count = Transaction.objects.count()
        transaction_data = {
            'Amount': '200.00',
            'Type': 'Expense',
            'Category': 'Category1',
        }
        print(str(self.category))
        
        response = self.client.post('/api/transactions/', transaction_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Transaction.objects.count(), initial_count + 1)
        # self.assertEqual(float(response.data['Amount']), float(transaction_data['Amount']))
        # self.assertEqual(response.data['Type'], transaction_data['Type'])
        # self.assertEqual(response.data['category'], str(self.category))
        # self.assertEqual(response.data['Date'], transaction_data['Date'])
        # self.assertEqual(response.data['user'], str(self.user.id))

    def test_retrieve_transaction(self):
        transaction_data = self.create_test_transaction()
        response = self.client.get(f'/api/transactions/{transaction_data["id"]}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['Amount']), float(transaction_data['Amount']))
        self.assertEqual(response.data['Type'], transaction_data['Type'])
        self.assertEqual(response.data['category'], str(self.category.id))
        self.assertEqual(response.data['Date'], transaction_data['Date'])
        self.assertEqual(response.data['user'], str(self.user.id))

    def test_update_transaction(self):
        transaction_data = self.create_test_transaction()
        url = f'/api/transactions/{transaction_data["id"]}/'
        updated_data = {
            'Amount': '150.00',
            'Type': 'E',
            'category': self.category.id,
            'Date': '2023-07-21T12:00:00Z',
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['Amount']), float(updated_data['Amount']))
        self.assertEqual(response.data['Type'], updated_data['Type'])
        self.assertEqual(response.data['category'], str(self.category.id))
        self.assertEqual(response.data['Date'], updated_data['Date'])
        self.assertEqual(response.data['user'], str(self.user.id))

    def test_delete_transaction(self):
        transaction_data = self.create_test_transaction()
        url = f'/api/transactions/{transaction_data["id"]}/'

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)



# class TransactionTestCase(APITestCase):
#     def setUp(self):
#         self.client = APIClient()
#         # Create a test user
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         # Generate JWT token for the user
#         self.token = str(RefreshToken.for_user(self.user).access_token)
#         # Include the token in the request headers
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

#     def test_create_transaction(self):
#         # Define the data for the new transaction
#         transaction_data = {'Amount': 100.0,'Type': 'Income','Category': 'Salary'}

#         # Make a POST request to create the transaction
#         response = self.client.post('/api/transactions/', transaction_data, format='json')
#         # Assert that the response status code is 201 (Created)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#         # Assert that the transaction was created successfully in the database
#         self.assertEqual(Transaction.objects.count(), 1)
#         self.assertEqual(response.data['Type'], 'Income')
#         self.assertIsNotNone(response.data['id'])  # Check if the 'id' field is present in the response

#     def test_retrieve_transaction(self):
#         # Create a sample transaction in the database
#         transaction = Transaction.objects.create(
#             user=self.user,
#             Amount="100.00",
#             Type='I',
#             Category='Salary',
#         )

#         # Make a GET request to retrieve the transaction
#         response = self.client.get(f'/api/transactions/{transaction.id}/')

#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Assert that the retrieved transaction's Type matches the created transaction's Type
#         self.assertEqual(response.data['Type'], transaction.get_Type_display())
#         self.assertEqual(response.data['id'], transaction.id)  # Check if the 'id' field is correct
#         self.assertEqual(response.data['Amount'], transaction.Amount)  # Check if the 'Amount' field is correct
#         self.assertEqual(response.data['Category'], transaction.Category)  # Check if the 'Category' field is correct

#     def test_update_transaction(self):
#         # Create a sample transaction in the database
#         transaction = Transaction.objects.create(
#             user=self.user,
#             Amount="100.00",
#             Type='I',
#             Category='Salary',
#         )

#         # Define the updated data for the transaction
#         updated_transaction_data = {
#             'Amount': '200.00',
#             'Type': 'Expense',
#             'Category': 'Bonus',
#         }

#         # Make a PUT request to update the transaction
#         response = self.client.put(f'/api/transactions/{transaction.id}/', updated_transaction_data, format='json')

#         # Assert that the response status code is 200 (OK)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Refresh the transaction from the database to get the latest changes
#         transaction.refresh_from_db()

#         # Assert that the transaction's fields have been updated correctly
#         self.assertEqual(transaction.Amount, Decimal("200.00"))
#         self.assertEqual(transaction.Type, 'E')
#         self.assertEqual(response.data['Type'], 'Expense')
#         self.assertEqual(response.data['id'], transaction.id)  # Check if the 'id' field is correct

#     def test_delete_transaction(self):
#         # Create a sample transaction in the database
#         transaction = Transaction.objects.create(
#             user=self.user,
#             Amount="100.00",
#             Type='I',
#             Category='Salary',
#         )

#         # Make a DELETE request to delete the transaction
#         response = self.client.delete(f'/api/transactions/{transaction.id}/')

#         # Assert that the response status code is 204 (No Content) since the object is deleted
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

#         # Assert that the transaction is deleted from the database
#         self.assertEqual(Transaction.objects.count(), 0)