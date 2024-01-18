import mysql.connector
from tabulate import tabulate

class BudgetHandler:
    def __init__(self, connection, user):
        self.user = user
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.user_id = self.get_user_id()

    def get_user_id(self):
        try:
            query = "SELECT id FROM Users WHERE username=%s;"
            self.cursor.execute(query, (self.user,))
            result = self.cursor.fetchone()
            if result is not None:
                return result[0]
            else:
                print(f'User {self.user} does not exist')
                return None
        except mysql.connector.Error as err:
            print(f'Something went wrong: {err}')

    def create_user(self):
        try:
            # check for existing user
            query = "SELECT id FROM Users WHERE username = %s;"
            self.cursor.execute(query, (self.user,))
            result = self.cursor.fetchone()

            if result is None:
                query = "INSERT INTO Users (username) VALUES (%s);"
                self.cursor.execute(query, (self.user,))
                self.connection.commit()
                self.user_id = self.get_user_id()
                print(f'Created new User: {self.user}')
            else:
                print(f'User {self.user} already exists')
        except mysql.connector.Error as err:
            print(f'Something went wrong: {err}')

    def set_category_budget(self, category, amount):
        try:
            # First, check if the category exists
            query = "SELECT id FROM Categories WHERE name=%s AND user_id=%s;"
            self.cursor.execute(query, (category, self.user_id))
            result = self.cursor.fetchone()

            if result is None:
                # If the category doesn't exist, create it
                query = "INSERT INTO Categories (name, budget, user_id) VALUES (%s, %s, %s);"
                self.cursor.execute(query, (category, amount, self.user_id))
            else:
                # If the category exists, update its budget
                category_id = result[0]
                query = "UPDATE Categories SET budget=%s WHERE id=%s;"
                self.cursor.execute(query, (amount, category_id))

            self.connection.commit()

            formatted_amount = "${:,.2f}".format(amount)
            print(f'Set budget for category {category} to {formatted_amount}')

        except mysql.connector.Error as err:
            print(f'Something went wrong: {err}')

    def check_budget(self):
        try:
            query= """
                SELECT
                    Categories.name as category,
                    Categories.budget - IFNULL(SUM(Transactions.amount), 0) AS remaining_budget
                FROM
                    Categories
                LEFT JOIN
                    Transactions ON Categories.id = Transactions.category_id
                WHERE
                    Categories.user_id = %s
                GROUP BY Categories.id;
            """
            params = (self.user_id,)
            self.cursor.execute(query, params)
            result = self.cursor.fetchall()

            total_remaining_budget = 0
            table_data = []

            for row in result:
                category, remaining_budget = row
                total_remaining_budget += remaining_budget
                table_data.append([category, "${:,.2f}".format(remaining_budget)])
                print(f'Your remaining budget for category {category} is ${remaining_budget:,.2f}')

            table_data.append(['Monthly Total', "${:,.2f}".format(total_remaining_budget)])

            print(tabulate(table_data, headers=['Category', 'Remaining Budget'], tablefmt='pretty'))

        except mysql.connector.Error as err:
            print(f'Something went wrong: {err}')

    def drop_category(self, category):
        try:
            # First, check if the category exists
            query = "SELECT id FROM Categories WHERE name=%s AND user_id=%s;"
            self.cursor.execute(query, (category, self.user_id))
            result = self.cursor.fetchone()

            if result is None:
                print(f'Category {category} does not exist')
            else:
                # If the category exists, delete it
                category_id = result[0]
                query = "DELETE FROM Categories WHERE id=%s;"
                self.cursor.execute(query, (category_id,))

                self.connection.commit()

                print(f'Dropped category {category}')

        except mysql.connector.Error as err:
            print(f'Something went wrong: {err}')




