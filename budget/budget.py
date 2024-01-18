import click
from db.db_handler import DBHandler
from budget.budget_handler import BudgetHandler

@click.command()
@click.argument('user')
@click.option('--new-user', is_flag=True, help='Create a new user.')
@click.option('--setup-budget', is_flag=True, help='Setup your monthly budget.')
@click.option('--create-transaction', nargs=2, type=(str, float), help='Create a new transaction give category and amount.')
@click.option('--drop-category', default=None, help='Drop a category from your budget.')
@click.option('--check', is_flag=True, help='Check your budget.')
def budget(user, check, new_user, setup_budget, drop_category, create_transaction):
    """
    This command allows a USER to manage their budget.

    USER is the name of the user.
    """

    try:
        # TODO: enter your database credentials.
        # for ease of use host and port are setup for a docker container running mysql:8
        db_handler = DBHandler(host="localhost", port=3306, user="root", password="my-secret-pw", database="budget_tool")
        connection = db_handler.get_connection()
        budget_handler = BudgetHandler(connection=connection, user=user)

        if new_user:
            budget_handler.create_user()

        if setup_budget:
            click.echo(f"Setting up {user}'s monthly budget")
            categories = []
            while True:
                category = click.prompt('Please enter a category name (or "exit" to stop)')
                if category.lower() == 'exit':
                    break

                amount = click.prompt('Please enter the budget amount for this category', type=float)
                categories.append((category, amount))

            budget_handler.set_category_budget(categories)

        if drop_category:
            click.echo(f'Dropping category {drop_category}')
            budget_handler.drop_category(drop_category)

        if create_transaction:
            category, amount = create_transaction
            click.echo(f'Creating a new transaction of ${amount} in category {category}')
            budget_handler.create_transaction(category, amount)

        if check:
            click.echo(f'Checking {user} budget')
            budget_handler.check_budget()

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        connection.close()

