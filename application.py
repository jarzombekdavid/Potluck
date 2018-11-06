import os
import pymysql
from flask import flash, redirect, render_template, request, session, jsonify
from flask_api import FlaskAPI, status, exceptions
from potluck_db_manager import PotluckDBManager

app = FlaskAPI(__name__)

db = PotluckDBManager()

@app.route('/api/login/', methods=['POST'])
def api_login():
    """allow login"""

    # pull out username and password
    email = request.form.get('email')
    password = request.form.get('password')

    result = db.get_user_data(email)

    if len(result) == 0:
        return {"user_id": "Invalid Request"}, status.HTTP_400_BAD_REQUEST
    elif result[0]['password'] == password:
        user_id = result[0]['user_id']
        return {"user_id": user_id}, status.HTTP_200_OK
    else:
        return {"user_id": "Invalid Request"}, status.HTTP_400_BAD_REQUEST

@app.route('/')
def index():

    placeholder = {"message": "hello"}
    return jsonify(placeholder)



@app.route('/api/register/', methods=["POST"])
def api_register_user():
    try:
        # add input validation
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        user_id = db.create_user(email=email,
                                 name=name,
                                 password=password)

        return {'user_id': user_id}, status.HTTP_201_CREATED
    except:
        return {'user_id': 'Invalid Request'}, status.HTTP_400_BAD_REQUEST


@app.route('/api/potlucks/<int:user_id>/', methods=['GET', 'POST', 'DELETE'])
def potlucks(user_id):
    '''Returns all potlucks for a given user
    '''
    if request.method == 'GET':
        data = db.get_user_potlucks(
            user_id=user_id
        )
        return data, status.HTTP_200_OK

if __name__ == "__main__":
    app.run(debug=True)
