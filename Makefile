# Makefile

# Имя Docker-контейнера
CONTAINER_NAME=mback

# Команда для создания пользователя
create_user:
	docker exec -it $(CONTAINER_NAME) python manage_users.py create --login $(LOGIN) --password $(PASSWORD)

# Команда для удаления пользователя
delete_user:
	docker exec -it $(CONTAINER_NAME) python manage_users.py delete --login $(LOGIN)

# Команда для просмотра списка пользователей
list_users:
	docker exec -it $(CONTAINER_NAME) python manage_users.py list



# Помощь
help:
	@echo "Доступные команды:"
	@echo "  make create_user LOGIN=<логин> PASSWORD=<пароль> - Создать нового пользователя"
	@echo "  make delete_user LOGIN=<логин>                   - Удалить пользователя"
	@echo "  make list_users                                  - Показать список всех пользователей"
