# helping functions
import os
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# get environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

# create database engine
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def connect_mysql(server='68.183.24.140'):

	engine_config = 'mysql+pymysql://{username}:{password}@{server}/potluck'.format(username=USERNAME,
                                                                            password=PASSWORD,
                                                                            server=server)

	engine = create_engine('mysql://{username}:{password}@{server}/potluck')

	return engine


def sql_create_user(email, password, name):

	query = '''insert into
			   users (full_name, email, `password`)
			   values ({full_name}, {email_address}, {password});
			   select LAST_INSERT_ID()'''.format(full_name=name,
	                              	             password=password,
	                              	             email=email)

	results = db.execute(query, multi=True)
	user_id = results.fetchone()

	return user_id


def sql_retrieve_user_data(email):

	query = '''select password, id
	           from users
	           where email = ''{}''
	           '''.format(email)

	results = db.execute(query)
	user_data = results.fetchone()

	return user_data


def sql_retrieve_profile_data(user_id):

	query = '''

	'''
