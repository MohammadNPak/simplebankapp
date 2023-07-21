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

