Фанатский сервер

Для отправки почты нужно в корне проекта создать файл
.env с содержимым:

EMAIL_HOST='smtp.domen.ru'
EMAIL_PORT=465
EMAIL_HOST_USER='user_name'
EMAIL_HOST_PASSWORD='123'
EMAIL_USE_SSL=True


Запуск Celery с выполнение по расписанию
celery -A fun_board worker -l INFO -B
