# IMPORTANT
# this code works on pythonanywhere, but might not quite work locally!!

from MySQLdb import connect
import click
from flask import current_app, g


def get_db():
    if 'db' not in g:
        g.db = connect("Turturicar.mysql.pythonanywhere-services.com","Turturicar","yr^6W]kEqB.CBdD","Turturicar$server-db")

    return g.db


def close_db(event):
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


def execute_sql_test_select():
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM users"
            cursor.execute(sql)
            result = cursor.fetchall()
            return result
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def execute_sql_insert_pwd(id_master_user, url_path, username, password):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO passwords (id_user, s_url_path, s_username, s_password) VALUES (%s, %s)"
            cursor.execute(sql, (id_master_user, url_path, username, password))
        db.commit()
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def execute_sql_select_pwd(id_master_user, url_path):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM passwords WHERE id_user=%s AND s_url_path=%s"
            cursor.execute(sql, (id_master_user, url_path))
            result = cursor.fetchall()
            return result
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def execute_sql_update_pwd(id_master_user, url_path, username, new_password):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "UPDATE passwords SET password = %s WHERE id_user = %s AND s_url_path = %s AND s_username = %s"
            cursor.execute(sql, (new_password, id_master_user, url_path, username))
            db.commit()
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def execute_sql_delete_pwd(id_master_user, url_path, username):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "DELETE FROM table_name WHERE id_user = %s AND s_url_path = %s AND s_username = %s;"
            cursor.execute(sql, (id_master_user, url_path, username))
            db.commit()
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def create_user_in_db(user, mail, password):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "INSERT INTO users (master_user, master_email, master_password) VALUES (%s, %s, %s)"
            cursor.execute(sql, (user, mail, password))
        db.commit()
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def check_user_in_db(usermail, password):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM users WHERE master_user = %s"
            cursor.execute(sql, usermail)
            result = cursor.fetchone()

            if not result:
                sql = "SELECT * FROM users WHERE master_email = %s"
                cursor.execute(sql, usermail)
                result = cursor.fetchone()

            # might raise an error because result is not checked if empty
            if password == result['master_password']:
                return True

            return False
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


@click.command('init-db')
def init_db_command():
    """Initialize database"""
    execute_sql_from_file('db_operations/script.sql')
    click.echo('Initialized the database.')


def init_db():
    """Initialize database"""
    execute_sql_from_file('db_operations/script.sql')
    return


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)