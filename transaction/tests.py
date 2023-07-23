from datetime import datetime, timedelta
from decimal import Decimal
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.test import TestCase
from .models import Transaction,Category
from rest_framework.test import APITestCase
from django.urls import reverse

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

    def create_test_transaction(self):
        transaction_data = {
            'Amount': '100.00',
            'Type': 'Income',
            'Category': str(self.category),
        }

        response = self.client.post('/api/transactions/', transaction_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response.data

    def test_create_transaction(self):
        initial_count = Transaction.objects.count()
        transaction_data = {
            'Amount': '200.00',
            'Type': 'Expense',
            'Category': str(self.category),
        }
        # print(str(self.category))
        
        response = self.client.post('/api/transactions/', transaction_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), initial_count + 1)
        self.assertEqual(float(response.data['Amount']), float(transaction_data['Amount']))
        self.assertEqual(response.data['Type'], transaction_data['Type'])
        self.assertEqual(response.data['Category'], str(self.category))
        self.assertEqual(response.data['Date'], Transaction.objects.last().Date)
        # self.assertEqual(response.data['user'], str(self.user.id))

    def test_retrieve_transaction(self):
        transaction_data = self.create_test_transaction()
        response = self.client.get(f'/api/transactions/{transaction_data["id"]}/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['Amount']), float(transaction_data['Amount']))
        self.assertEqual(response.data['Type'], transaction_data['Type'])
        self.assertEqual(response.data['Category'], str(self.category))
        self.assertEqual(response.data['Date'], transaction_data['Date'])

    def test_update_transaction(self):
        transaction_data = self.create_test_transaction()
        url = f'/api/transactions/{transaction_data["id"]}/'
        updated_data = {
            'Amount': '150.00',
            'Type': 'Expense',
            'Category': str(self.category),
        }

        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['Amount']), float(updated_data['Amount']))
        self.assertEqual(response.data['Type'], updated_data['Type'])
        self.assertEqual(response.data['Category'], str(self.category))

    def test_delete_transaction(self):
        transaction_data = self.create_test_transaction()
        url = f'/api/transactions/{transaction_data["id"]}/'

        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)


class MonthlySummaryReportTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create sample categories
        self.category1 = Category.objects.create(name='Category1')
        self.category2 = Category.objects.create(name='Category2')

        # Create sample transactions for the current month
        today = datetime.now()
        first_day_of_month = today.replace(day=1)
        last_day_of_month = (first_day_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        Transaction.objects.create(user=self.user, Amount='100.00', Type='I', Category=self.category1, Date=today)
        Transaction.objects.create(user=self.user, Amount='50.00', Type='E', Category=self.category1, Date=today)
        Transaction.objects.create(user=self.user, Amount='200.00', Type='I', Category=self.category2, Date=today)
        Transaction.objects.create(user=self.user, Amount='75.00', Type='E', Category=self.category2, Date=today)

    def test_monthly_summary_report(self):
        # Ensure the monthly summary report works correctly
        url = reverse('monthly_summary_report')

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], 'testuser')
        self.assertEqual(response.data['month'], datetime.now().strftime('%B %Y'))
        self.assertEqual(response.data['total_income'], 300.00)
        self.assertEqual(response.data['total_expenses'], 125.00)
        self.assertEqual(response.data['net_cash_flow'], 175.00)
        self.assertEqual(len(response.data['expense_income_by_category']), 2)  # Assuming you have two categories

    def test_monthly_summary_report_no_data(self):
        # Ensure the monthly summary report returns no data for a month with no transactions
        # First, delete the transactions created in the setup function to simulate no data
        Transaction.objects.all().delete()

        url = reverse('monthly_summary_report')

        self.client.force_authenticate(user=self.user)
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['user'], 'testuser')
        self.assertEqual(response.data['month'], datetime.now().strftime('%B %Y'))
        self.assertEqual(response.data['total_income'], 0)
        self.assertEqual(response.data['total_expenses'], 0)
        self.assertEqual(response.data['net_cash_flow'], 0)
        self.assertEqual(response.data['expense_income_by_category'], "No Data")
