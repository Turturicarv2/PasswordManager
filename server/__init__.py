import os

from flask import Flask, Response, render_template, jsonify
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
    
    @app.route('/test_insert/')
    def test_insert():
        db.execute_sql_from_file('insert.sql')
        return 'Inserted!'

    @app.route('/test_select/')
    def test_select():
        result = db.execute_sql_from_file('select.sql')
        return render_template('select.html', result=result)
    
    @app.route('/get_data/')
    def get_data():
        result = db.execute_sql_from_file('select.sql')
        return jsonify(result=result)
    
    @app.route('/store_pwd/<path>/')
    def store_pwd(path):
        db.execute_sql_insert_pwd(path=path)
        return
    
    @app.route('/return_pwd/<path>/')
    def return_pwd(path):
        result = db.execute_sql_select_pwd(path=path)
        return jsonify(result=result)

    return app

application = create_app()