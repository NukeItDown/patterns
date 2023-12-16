from settings import db, app, migrate
from models import *

#db.init_app(app)
migrate.init_app(app, db)

# export FLASK_APP=manage.py
# Инициализация:            flask db init
# Подготовка к миграции:    flask db migrate
# Миграция:                 flask db upgrade

