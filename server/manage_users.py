# manage_users.py
import argparse
from db.session import get_db, engine, Base
from models import User, Site
from db.crud import create_user


Base.metadata.create_all(bind=engine)

def create_user_cli(login: str, password: str):
    """Creates a new user through the console."""
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    existing_user = db.query(User).filter(User.login == login).first()
    if existing_user:
        print(f"A user with the login '{login}' already exists.")
        return
    try:
        user = create_user(db, login=login, password=password)
        print(f"User '{user.login}' has been successfully created.")
    except Exception as e:
        print(f"Error creating the user: {e}")

def delete_user_cli(login: str):
    """Deletes the user by login."""
    db = next(get_db())
    user = db.query(User).filter(User.login == login).first()
    if not user:
        print(f"User with the login '{login}' not found.")
        return
    db.delete(user)
    db.commit()
    print(f"User '{login}' has been successfully deleted.")

def list_users_cli():
    """Displays a list of all users."""
    db = next(get_db())
    users = db.query(User).all()
    if not users:
        print("No users yet")
        return
    print(f"{'ID':<5} {'Login':<20} {'Active':<10}")
    print("-" * 35)
    for user in users:
        print(f"{user.id:<5} {user.login:<20} {str(user.is_active):<10}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="User management through the console.")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Command to create a user.
    create_parser = subparsers.add_parser("create", help="Create a new user.")
    create_parser.add_argument("--login", required=True, help="Login")
    create_parser.add_argument("--password", required=True, help="Password")

    # Command to delete a user.
    delete_parser = subparsers.add_parser("delete", help="Delete user")
    delete_parser.add_argument("--login", required=True, help="Login")

    # Command to view the list of users.
    subparsers.add_parser("list", help="Users list")

    args = parser.parse_args()

    if args.command == "create":
        create_user_cli(args.login, args.password)
    elif args.command == "delete":
        delete_user_cli(args.login)
    elif args.command == "list":
        list_users_cli()
    else:
        parser.print_help()