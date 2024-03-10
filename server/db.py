import pymysql
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        timeout = 10

        g.db = pymysql.connect(
            charset="utf8mb4",
            connect_timeout=timeout,
            cursorclass=pymysql.cursors.DictCursor,
            db="Flask",
            host="mysql-2ccb2f6c-daniel-f835.a.aivencloud.com",
            password="AVNS_p-vlOmU1uY0VsjX-AOc",
            read_timeout=timeout,
            port=20945,
            user="avnadmin",
            write_timeout=timeout,
        )

    return g.db


def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


def execute_sql_from_file(filename):
    db = get_db()

    with current_app.open_resource(filename) as f:
        sql_commands = f.read().decode('utf8').split(';')
        try:
            with db.cursor() as cursor:
                for command in sql_commands:
                    if command.strip():
                        cursor.execute(command)
                        if command.strip().lower().startswith('select'):
                            result = cursor.fetchall()
                            return result
            db.commit()
        except Exception as e:
            # Print or log the error message
            print("Error executing SQL commands:", e)
            # Rollback any changes if necessary
            db.rollback()
            # Optionally raise the exception to halt execution
            raise


def execute_sql_insert_pwd(path):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO passwords (column1, column2) VALUES (%s, %s)"
            cursor.execute(sql, (path, 'value2'))  # You can change 'value2' here or make it another parameter
        db.commit()
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def execute_sql_select_pwd(path):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "SELECT FROM passwords (column1, column2) VALUES (%s, %s)"
            cursor.execute(sql, (path, 'value2'))  # You can change 'value2' here or make it another parameter
        db.commit()
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    execute_sql_from_file('script.sql')
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)