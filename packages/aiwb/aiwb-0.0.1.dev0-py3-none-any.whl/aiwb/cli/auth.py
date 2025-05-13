import click

@click.command()
@click.pass_obj
def login(session):
    res = session.generate_auth_token()
    if res:
        print("\nlogin successfully")

@click.command()
@click.pass_obj
def logout(session):
    res = session.revoke_auth_token()
    if res:
        print("\nlogout successfully")

@click.command()
@click.pass_obj
def whoami(session):
    print(session.user_info())