# IMPORTANT
# this code works on pythonanywhere, but might not quite work locally!!
from flask import Flask, jsonify, request
from flask_cors import CORS

from db import *

# create and configure the server
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
    SECRET_KEY='dev'
)
CORS(app)

init_app(app)

# routing
@app.route('/')
def home():
    init_db()
    return "Hello! Check the extension!"

@app.route('/get_data/')
def get_data():
    result = execute_sql_test_select()
    return jsonify(result=result)

@app.route('/get_master_user/', methods = ['GET'])
def get_master_user():
    id_master_user = request.args.get('id_user')
    result = execute_sql_select_master_user(id_master_user)
    return jsonify(result)

@app.route('/store_pwd/', methods = ['POST'])
def store_pwd():
    id_master_user = request.args.get('id_user')
    url_path = request.args.get('url_path')
    username = request.args.get('username')
    password = request.args.get('password')
    execute_sql_insert_pwd(id_master_user=id_master_user, url_path=url_path, username=username, password=password)
    return

@app.route('/select_pwd/', methods = ['GET'])
def select_pwd():
    id_master_user = request.args.get('id_user')
    url_path = request.args.get('url_path')
    result = execute_sql_select_specific_pwd(id_master_user=id_master_user, url_path=url_path)
    return jsonify(result=result)

@app.route('/select_all_pwd/', methods = ['GET'])
def select_all_pwd():
    id_master_user = request.args.get('id_user')
    result = execute_sql_select_all_pwd(id_master_user=id_master_user)
    return jsonify(result=result)

@app.route('/update_pwd/', methods = ['PUT'])
def update_pwd():
    password_id = request.args.get('password_id')
    username = request.args.get('username')
    new_password = request.args.get('password')
    return execute_sql_update_pwd(id_password = password_id, username=username, new_password=new_password)

@app.route('/delete_pwd/', methods = ['DELETE'])
def delete_pwd():
    password_id = request.args.get('password_id')
    return execute_sql_delete_pwd(password_id)

@app.route('/create_user/', methods = ['POST'])
def create_user():
    try:
        username = request.args.get('username')
        email = request.args.get('email')
        password = request.args.get('password')

        result = create_user_in_db(user=username, mail=email, password=password)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/authenticate_user/', methods = ['GET'])
def authenticate_user():
    usermail = request.args.get('usermail')
    password = request.args.get('password')
    return check_user_in_db(usermail=usermail, password=password)

if __name__ == '__main__':
    app.run()