import os
import pymysql
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from potluck_db_manager import PotluckDBManager

app = Flask(__name__)


db = PotluckDBManager()

@app.route('/api/login/', methods=['POST'])
def api_login():

    # pull out username and password
    email = request.form.get('email')
    password = request.form.get('password')

    result = db.get_user_data(email)
    user_id = result[0]['user_id']

    if len(result) == 0:
        return jsonify({"user_id": "Invalid Request"})
    elif result[0]['password'] == password:
        return jsonify({"user_id": "{}".format(user_id)})
    else:
        return jsonify({"user_id": "Invalid Request"})


@app.route('/', methods=['GET'])
def index():

    placeholder = {"message": "hello"}
    return jsonify(placeholder)



@app.route('/api/signup/', methods=['POST'])
def api_create_user():
    # add input validation
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user_id = db.create_user(email=email,
                                   name=name,
                                   password=password)

        return jsonify(user_id)



@app.route('/profile')
def user_profile(user_id):
    return 'User Profile Potluck Page'



@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = validate_login(email=request.form.email,
                            password = request.form.password)
        return jsonify(data)



@app.route('/potlucks', methods=['POST'])
def potlucks():
    '''Returns all potlucks for a given user
    '''
    if request.method == 'POST':
        data = db.get_user_potlucks(user_id=request.form['user_id'])
        return jsonify(data)


if __name__ == "__main__":
    app.run(debug=True)
