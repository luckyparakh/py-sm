1.  Create venv
    python3 -m venv venv
2.  Then set interpreter of project as './fastapi/venv/bin/python' by CTRL+Shift+P -> Python Interpreter
3. GO to terminal & type ' cd fastapi && source venv/bin/activate '
4.  pip install fastapi[all]
5.  uvicorn app.main:app --reload
6.  pip install "psycopg" 
7.  pip install "passlib[bcrypt]"
8.  pip install pyjwt
9.  pip install alembic