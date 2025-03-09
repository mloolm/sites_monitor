# manage_users.py
import argparse
from sqlalchemy.orm import Session
from db.session import get_db, engine, Base
from models import User, Site
from db.crud import create_user


Base.metadata.create_all(bind=engine)

def create_user_cli(login: str, password: str):
    """Создает нового пользователя через консоль."""
    Base.metadata.create_all(bind=engine)
    db = next(get_db())
    existing_user = db.query(User).filter(User.login == login).first()
    if existing_user:
        print(f"Пользователь с логином '{login}' уже существует.")
        return
    try:
        user = create_user(db, login=login, password=password)
        print(f"Пользователь '{user.login}' успешно создан.")
    except Exception as e:
        print(f"Ошибка при создании пользователя: {e}")

def delete_user_cli(login: str):
    """Удаляет пользователя по логину."""
    db = next(get_db())
    user = db.query(User).filter(User.login == login).first()
    if not user:
        print(f"Пользователь с логином '{login}' не найден.")
        return
    db.delete(user)
    db.commit()
    print(f"Пользователь '{login}' успешно удален.")

def list_users_cli():
    """Выводит список всех пользователей."""
    db = next(get_db())
    users = db.query(User).all()
    if not users:
        print("Пользователи не найдены.")
        return
    print(f"{'ID':<5} {'Логин':<20} {'Активен':<10}")
    print("-" * 35)
    for user in users:
        print(f"{user.id:<5} {user.login:<20} {str(user.is_active):<10}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Управление пользователями через консоль.")
    subparsers = parser.add_subparsers(dest="command", help="Команды")

    # Команда для создания пользователя
    create_parser = subparsers.add_parser("create", help="Создать нового пользователя")
    create_parser.add_argument("--login", required=True, help="Логин пользователя")
    create_parser.add_argument("--password", required=True, help="Пароль пользователя")

    # Команда для удаления пользователя
    delete_parser = subparsers.add_parser("delete", help="Удалить пользователя")
    delete_parser.add_argument("--login", required=True, help="Логин пользователя")

    # Команда для просмотра списка пользователей
    subparsers.add_parser("list", help="Список всех пользователей")

    args = parser.parse_args()

    if args.command == "create":
        create_user_cli(args.login, args.password)
    elif args.command == "delete":
        delete_user_cli(args.login)
    elif args.command == "list":
        list_users_cli()
    else:
        parser.print_help()