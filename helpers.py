from sql_functions import sql_retrieve_user_data
from sql_functions import sql_create_user
from sql_functions import sql_retrieve_profile_data


def create_user(email, password, name):

    user_data = {}

    user_id = sql_create_user(email, password, name)

    user_data['user_id'] = 'user_id'

    return user_id


def validate_login(email, password):

    user_data = sql_retrieve_user_data(email)
    validation = {}

    #if len(user_data) != 1 or not check_password_hash(user_data[0]["hash"], password):
    if len(user_data) != 2 or not user_data[0] == password:
        validation['status'] = False
        validation['user_id'] = -1
    else:
        validation['status'] = True
        validation['user_id'] = user_data[1]

    return validation



def retrieve_user_profile_data(user_id):

    data = sql_retrieve_profile_data(user_id)
