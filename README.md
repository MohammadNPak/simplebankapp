# Instructions:
Your task is to build a Restful API for a cash management system using Django and Django Rest Framework. The system should allow users to manage their cash flow by creating and updating transactions, tracking balances, and generating reports.
Requirements:
1. User Authentication:
- Users should be able to register and authenticate themselves using a username and password.
- Only authenticated users should be able to access the API endpoints.
2. Transaction Management:
- Users should be able to create, retrieve, update, and delete transactions.
- Each transaction should include the following information:
    - Amount: The amount of money involved in the transaction.
    - Type: The type of transaction (e.g., income, expense).
    - Category: The category of the transaction (e.g., groceries, utilities).
    - Date: The date of the transaction.
- Users should be able to filter and sort transactions based on different criteria (e.g., date, category).
3. Balance Tracking:
- The system should keep track of the user's balance by calculating the current balance based on the transactions.
- The balance should be updated automatically whenever a new transaction is created or updated.
4. Reports:
- Users should be able to generate reports to analyze their cash flow.
- The system should provide at least one type of report, such as a monthly summary or a category-wise expense report.
5. Unit Testing and Integration Testing:
- Write comprehensive unit tests and integration tests for the different components and functionalities of the system.
6. Dockerization:
- Dockerize the application to ensure easy deployment and portability.
# Deliverables:
- A Django project that includes the Restful API for the cash management system.
- A README file with instructions on how to set up and run the project.
- Unit tests and integration tests for the implemented functionalities.
- Docker configuration files to containerize the application.


# Evaluation Criteria:
- Proper usage of Django and Django Rest Framework.
- Correct implementation of API endpoints with appropriate request/response handling.
- Effective data modeling and database interaction.
- Thorough unit testing and integration testing.
- Adherence to RESTful API concepts and best practices.
- Accuracy and efficiency in cash flow calculations and balance tracking.
- Well-documented code and clear instructions in the README file.
- Successful Dockerization of the application.



# simple bank transactions

This is a Django project that provides a simple and efficient way to manage personal transactions, generate monthly summary reports, and analyze cash flow. It uses Django Rest Framework for building the API and JWT (JSON Web Token) for user authentication.

## Features

- User Registration: New users can register and create their accounts to access the application.
- User Authentication: Registered users can log in securely using their credentials.
- Transaction Management: Users can create, view, update, and delete their transactions.
- Monthly Summary Report: Users can generate a monthly summary report of their cash flow, including total income, total expenses, net cash flow, and category-wise income and expenses.
- Category Management: Users can create and manage categories for organizing their transactions.
- Docker Compose: The project includes a Docker Compose file for easy deployment and containerization.

## How to Run

To run the project using Docker Compose, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/mohammadnpak/queradjango.git
cd queradjango
```

2. Set up the environment variables (optional):

Create a `.env` file in the project root directory and add the following environment variables:

```dotenv
SECRET_KEY=mysecretkey
DEBUG=True
DB_NAME=mydatabase
DB_USER=mydbuser
DB_PASSWORD=mydbpassword
DB_HOST=db
DB_PORT=5432
```

Replace the values with your preferred settings. The `SECRET_KEY` should be a strong secret key for Django.

3. Build and run the Docker containers (only necessary step):

```bash
docker-compose build
docker-compose up -d
```

4. Apply database migrations:

```bash
docker-compose exec web python manage.py migrate
```

5. Create a superuser (admin):

```bash
docker-compose exec web python manage.py createsuperuser
```

Follow the prompts to set the superuser's username, email, and password.

6. Access the application:

The Django project will be running at `http://localhost:8000/`. You can access the Django admin interface at `http://localhost:8000/admin/` and log in using the superuser credentials created in the previous step.

## API Endpoints

The following API endpoints are available:

- `POST /api/token/`: Obtain a JWT access and refresh token by providing valid user credentials (username and password).
- `POST /api/token/refresh/`: Refresh the JWT access token by providing a valid refresh token.
- `POST /api/register/`: create new user with username and password and return access token and refresh token
- `GET /api/transactions/`: Retrieve a list of all transactions.
- `POST /api/transactions/`: Create a new transaction.
- `GET /api/transactions/{id}/`: Retrieve a specific transaction by ID.
- `PUT /api/transactions/{id}/`: Update a specific transaction by ID.
- `DELETE /api/transactions/{id}/`: Delete a specific transaction by ID.
- `GET /api/categories/`: Retrieve a list of all categories.
- `POST /api/categories/`: Create a new category.
- `GET /api/categories/{id}/`: Retrieve a specific category by ID.
- `PUT /api/categories/{id}/`: Update a specific category by ID.
- `DELETE /api/categories/{id}/`: Delete a specific category by ID.
- `GET /api/report/monthly/`: Generate a monthly summary report of cash flow.
- `GET /api/report/current_balance/`: Generate current amount of balance of user.


## Contributing

Contributions to this project are welcome! If you find any bugs, have feature requests, or want to contribute code, please feel free to create an issue or a pull request on GitHub.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---
