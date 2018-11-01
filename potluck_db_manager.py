import os
import pymysql

class DBManager:
    """Class to handle all database functions"""

    def __init__(self, host=None, database=None, user=None, password=None):

        # if no configs provided, use system configs
        if host is None:
            self.host = os.getenv("HOST")
        else:
            self.host = host

        if database is None:
            self.database = os.getenv("DATABASE")
        else:
            self.database = database

        if user is None:
            self.user = os.getenv("USER")
        else:
            self.user = user

        if password is None:
            self.password = os.getenv("PASSWORD")
        else:
            self.password = password

        self.connect()

    def connect(self):
        """Connect to database"""

        self.conn = pymysql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )

        # TODO: this feels like an unnecessary hook
        self.create_cursor()


    def create_cursor(self):
        """Create a cursor if one doesn't exist"""
        self.cursor = self.conn.cursor()

    def execute(self, query, parameters=None):
        """Execute a query"""

        try:
            self.cursor.execute(query, parameters)
            return self.cursor.fetchall()

        except (pymysql.InterfaceError, pymysql.InternalError):
            # retry with a new connection
            self.close()
            self.connect()
            self.cursor.execute(query, parameters)
            self.cursor.fetchall()

    def commit(self):
        """Commit connection"""
        self.conn.commit()

    def close(self):
        self.conn.close()

class PotluckDBManager(DBManager):
    """Potluck Database Manager"""

    def create_user(self, email, password, name):
        """Create a user"""


        query = """INSERT INTO
                   users (full_name, email, `password`)
                   values ('{full_name}', '{email}', '{password}');
        """.format(
            full_name=name,
            password=password,
            email=email
        )

        self.execute(query)
        user_id = self.get_last_id()
        self.commit()

        return user_id


    def get_last_id(self):
        """Get last user id"""
        last_id_dict = self.execute("SELECT LAST_INSERT_ID() as ID")
        last_id = last_id_dict[0]['ID']

        return last_id

    def get_user_data(self, email):
        """Validate user login information"""
        query = """select password, user_id
                   from users
                   where email = '{}'
                """.format(email)

        return self.execute(query)

    def get_user_potlucks(self, user_id):
        """Get profile data for given user id

            Includes potluck information about potlucks they are a part of
            or have been to
        """

        query1 = """select potluck_id,
                           potluck_name,
                           potluck_date,
                           potluck_description,
                           potluck_location,
                           case when host_user_id = {user_id} then 1
                           else 0 end as IsHost
                    from potluck
                    where potluck_id in (select potluck_id
                                         from potluck_users
                                         where user_id = {user_id}
                                         and user_status <> -1)

        """.format(user_id=user_id)

        data=self.execute(query1)
        self.commit()

        return data

    def get_user_dishes(self, user_id):
        """Get profile data for given user id

            Includes potluck information about potlucks they are a part of
            or have been to
        """
        #TO DO this is not right
        query1 = """select potluck_id,
                           potluck_name,
                           potluck_date,
                           case when host_user_id = {user_id} then 1
                           else 0 end as hosted
                    from potluck
                    where potluck_id in (select potluck_id
                                         from potluck_users
                                         where user_id = {user_id}
                                         and rejected <> 1)

        """.format(user_id=user_id)

        data=self.execute(query1)
        self.commit()

        return data

    def create_potluck(self, user_id, potluck_name, potluck_date):
        """Create a potluck"""

        query1 = """insert into potluck.potluck (potluck_name, potluck_date, host_user_id)
                    values ('{potluck_name}', '{potluck_date}', {user_id})
        """.format(
            potluck_name=potluck_name,
            potluck_date=potluck_date,
            user_id=user_id
        )

        self.execute(query1)

        potluck_id = self.get_last_id()

        query2 = """insert into potluck.potluck_users (potluck_id, user_id, invited, rejected, accepted)
                    values ({potluck_id}, {user_id}, 0, 0, 0)
        """.format(
            potluck_id=potluck_id,
            user_id=user_id
        )

        self.execute(query2)

        self.commit()

        return potluck_id

    def invite_guest(self, potluck_id, guest_id):
        """Add a guest to a potluck"""

        query = """insert into potluck.potluck_users (potluck_id, user_id, invited, rejected, accepted)
                   values ({potluck_id}, {guest_id}, 1, 0, 0)
        """.format(potluck_id=potluck_id, guest_id=guest_id)

        self.execute(query)

        self.commit()
