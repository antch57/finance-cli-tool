import click

# Helper functions
def subtract_from_budget(subtract, user):
    click.echo(f'Subtracting {subtract} from {user} budget')


def add_to_budget(add, user):
    click.echo(f'Adding {add} to {user} budget')


def check_budget(check, user):
    click.echo(f'Checking {user} budget')
    click.echo(f'i am check: {check}')

@click.command()
@click.argument('user')
@click.option('--add', default=0, help='Amount to add to your budget.')
@click.option('--subtract', default=0, help='Amount to subtract from your budget.')
@click.option('--check', is_flag=True, help='Check your budget.')
def budget(user, add, subtract, check):
    """
    This command allows a USER to manage their budget.

    USER is the name of the user.
    """

    if add:
        add_to_budget(add, user)
    if subtract:
        subtract_from_budget(subtract, user)
    if check:
        check_budget(check, user)

if __name__ == '__main__':
    budget()

