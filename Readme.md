#### Python 3.9.13

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

#####
if you get error ->
    aiogram File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.1008.0_x64__qbz5n2kfra8p0\Lib\asyncio\events.py", line 88, in _run self._context.run(self._callback, *self._args) TypeError: 'Task' object is not callableaiogram File "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.12_3.12.1008.0_x64__qbz5n2kfra8p0\Lib\asyncio\events.py", line 88, in _run self._context.run(self._callback, *self._args) TypeError: 'Task' object is not callable

solution ->
    double click Shift -> Actions -> Registry
    next, remove checkbox from -> python.debug.asyncio.repl
