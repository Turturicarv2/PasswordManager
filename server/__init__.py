# IMPORTANT
# this code works on pythonanywhere, but might not quite work locally!!
from flask import Flask, jsonify, request
from flask_cors import CORS

from db import *

# create and configure the app
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

@app.route('/get_data_hosted/')
def get_data_hosted():
    result = execute_sql_test_select()
    return jsonify(result=result)

@app.route('/store_pwd/', methods = ['POST'])
def store_pwd():
    id_master_user = request.form('id_user')
    url_path = request.form('url_path')
    username = request.form('username')
    password = request.form('password')
    execute_sql_insert_pwd(id_master_user=id_master_user, url_path=url_path, username=username, password=password)
    return

@app.route('/return_pwd/', methods = ['GET'])
def return_pwd():
    id_master_user = request.args.get('id_user')
    url_path = request.args.get('url_path')
    result = execute_sql_select_pwd(id_master_user=id_master_user, url_path=url_path)
    return jsonify(result=result)

@app.route('/update_pwd/', methods = ['PUT'])
def update_pwd():
    id_master_user = request.args.get('id_user')
    url_path = request.args.get('url_path')
    username = request.args.get('username')
    new_password = request.args.get('new_password')
    return execute_sql_update_pwd(id_master_user=id_master_user, url_path=url_path, username=username, new_password=new_password)

@app.route('/delete_pwd/', methods = ['DELETE'])
def delete_pwd():
    id_master_user = request.args.get('id_user')
    url_path = request.args.get('url_path')
    username = request.args.get('username')
    execute_sql_delete_pwd(id_master_user=id_master_user, url_path=url_path, username=username)
    return

@app.route('/create_user/', methods = ['POST'])
def create_user():
    username = request.form('username')
    password = request.form('password')
    email = request.form('email')
    return create_user_in_db(user=username, mail=email, password=password)

@app.route('/authenticate_user/', methods = ['GET'])
def authenticate_user():
    usermail = request.args.get('usermail')
    password = request.args.get('password')
    return check_user_in_db(usermail=usermail, password=password)

if __name__ == '__main__':
    app.run()