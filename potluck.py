import os

from Potluck.helpers import validate_login
from flask import Flask, flash, redirect, render_template, request, session, jsonify

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return '{"message":"hello"}'


@app.route('/signup', methods=['POST'])
def create_user():
    # add input validation
    if request.method == 'POST':
        user_data = create_user(email=request.email,
                               full_name = request.full_name,
                               password = request.password)
        return(user_id)



@app.route('/profile')
def user_profile(user_id):
    return 'User Profile Potluck Page'


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        validation_data = validate_login(email=request.form.email,
                                         password = request.form.password)
        

        return validation_data

@app.route('/potluck')
def potluck_dishes():
    return 'Dishes associated with potluck'


if __name__ == "__main__":
    app.run(debug=True)

