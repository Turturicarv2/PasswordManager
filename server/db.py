# IMPORTANT
# this code works on pythonanywhere, but might not quite work locally!!
from MySQLdb import connect
import click
from flask import current_app, g


def verify_password(password, stored_hash):
    return password == stored_hash

def get_db():
    if 'db' not in g:
        g.db = connect("OtherTurt.mysql.pythonanywhere-services.com","OtherTurt","yr^6W]kEqB.CBdD","OtherTurt$server-db")
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
            rows = cursor.fetchall()

            if rows:
                # Get column names
                columns = [column[0] for column in cursor.description]

                # Convert each row to a dictionary
                result = []
                for row in rows:
                    row_dict = dict(zip(columns, row))
                    result.append(row_dict)

                return result
            else:
                return {"error": "No users found"}
    except Exception as e:
        # Rollback any changes
        db.rollback()
        return {"error": str(e)}


def execute_sql_select_master_user(id_master_user):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "SELECT master_user FROM users WHERE id_user=%s"
            cursor.execute(sql, (id_master_user,))
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
            sql = "INSERT INTO passwords (id_user, s_url_path, s_username, s_password) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_master_user, url_path, username, password))
        db.commit()
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def execute_sql_select_specific_pwd(id_master_user, url_path):
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


def execute_sql_select_all_pwd(id_master_user):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "SELECT * FROM passwords WHERE id_user=%s"
            cursor.execute(sql, (id_master_user,))
            result = cursor.fetchall()
            return result
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def execute_sql_update_pwd(id_password, username, new_password):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "UPDATE passwords SET s_password=%s, s_username=%s WHERE id_password = %s"
            cursor.execute(sql, (new_password, username, id_password))
            db.commit()

            return {"success": True}
    except Exception as e:
        # Print or log the error message
        print("Error executing SQL insert statement:", e)
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def execute_sql_delete_pwd(id_password):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "DELETE FROM passwords WHERE id_password = %s;"
            cursor.execute(sql, (id_password, ))
            db.commit()

            return {"success": True}
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
            # Check if the username or email already exists in the database
            sql_check_username = "SELECT COUNT(*) FROM users WHERE master_user = %s"
            cursor.execute(sql_check_username, (user,))
            username_result = cursor.fetchone()

            sql_check_email = "SELECT COUNT(*) FROM users WHERE master_email = %s"
            cursor.execute(sql_check_email, (mail,))
            email_result = cursor.fetchone()

            # If username already exists, return failure message
            if username_result[0] > 0:
                return {'success': False, 'message': 'Username already taken'}

            # If email already exists, return failure message
            if email_result[0] > 0:
                return {'success': False, 'message': 'Email already in use'}

            # If both username and email are unique, proceed with insertion
            sql_insert = "INSERT INTO users (master_user, master_email, master_password) VALUES (%s, %s, %s)"
            cursor.execute(sql_insert, (user, mail, password))

        db.commit()
        return {'success': True}
    except:
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        raise


def check_user_in_db(usermail, password):
    db = get_db()

    try:
        with db.cursor() as cursor:
            sql = "SELECT id_user, master_password FROM users WHERE master_user = %s"
            cursor.execute(sql, (usermail,))
            result = cursor.fetchone()

            if not result:
                sql = "SELECT id_user, master_password FROM users WHERE master_email = %s"
                cursor.execute(sql, (usermail,))
                result = cursor.fetchone()

            if not result:
                return_json = {"success": False, "message": "Wrong username or email"}
            else:
                password_match = verify_password(password, result[1])
                if password_match:
                    return_json = {"success": True, "id": result[0]}
                else:
                    return_json = {"success": False, "message": "Wrong password!"}

            return return_json

    except Exception as e:
        # Rollback any changes if necessary
        db.rollback()
        # Optionally raise the exception to halt execution
        return_data = {"success": False, "message": str(e)}
        return return_data


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