import os

from flask import Flask, Response, render_template, jsonify, request
from flask_cors import CORS

from . import db

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    CORS(app)
    
    db.init_app(app)

    @app.route('/')
    def home():
        return 'Hello! Check the extension!'
    
    @app.route('/get_data/')
    def get_data():
        result = db.execute_sql_from_file('db_operations/select.sql')
        return jsonify(result=result)
    
    @app.route('/store_pwd/', methods = ['POST'])
    def store_pwd():
        id_master_user = request.form('id_user')
        url_path = request.form('url_path')
        username = request.form('username')
        password = request.form('password')
        db.execute_sql_insert_pwd(id_master_user=id_master_user, url_path=url_path, username=username, password=password)
        return
    
    @app.route('/return_pwd/<path>/', methods = ['GET'])
    def return_pwd():
        id_master_user = request.args.get('id_user')
        url_path = request.args.get('url_path')
        result = db.execute_sql_select_pwd(id_master_user=id_master_user, url_path=url_path)
        return jsonify(result=result)
    
    @app.route('', methods = ['PUT'])
    def update_pwd():
        id_master_user = request.args.get('id_user')
        url_path = request.args.get('url_path')
        username = request.args.get('username')
        new_password = request.args.get('new_password')
        return db.execute_sql_update_pwd(id_master_user=id_master_user, url_path=url_path, username=username, new_password=new_password)
    
    @app.route('/create_user/', methods = ['POST'])
    def create_user():
        username = request.form('user')
        password = request.form('password')
        email = request.form('email')
        db.create_user_in_db(user=username, mail=email, password=password)
        return

    @app.route('/authenticate_user/', methods = ['GET'])
    def authenticate_user():
        usermail = request.args.get('usermail')
        password = request.args.get('password')
        return db.check_user_in_db(usermail=usermail, password=password)

    return app

if __name__ == '__main__':
    application = create_app()