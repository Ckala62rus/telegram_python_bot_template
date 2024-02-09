### Install all dependencies
```Bash
pip install -r requirements.txt
```

### Migrations
```Bash
alembic init migrations
alembic revision --autogenerate -m "init"
alembic upgrade head
alembic history
alembic downgrade 8ac14e223d1e

alembic downgrade base # delete all migration (Drop database)
```

###
```Bash
venv\Scripts\activate
```