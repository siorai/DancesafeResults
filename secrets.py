import os
import psycopg2


PG_HOST = os.environ["PG_HOST"]
PG_DB = os.environ["PG_DB"]
PG_USER = os.environ["PG_USER"]
PG_PASS = os.environ["PG_PASS"]
PG_PORT= os.environ["PG_PORT"]




def DBConn():
    
    pgConnection = psycopg2.connect(host=PG_HOST, 
                                    database=PG_DB,
                                    user=PG_USER,
                                    password=PG_PASS,
                                    port=PG_PORT)
    return pgConnection

pgConnection = psycopg2.connect(host=PG_HOST, 
                                database=PG_DB,
                                user=PG_USER,
                                password=PG_PASS,
                                port=PG_PORT)

class Postgres(object):
    """docstring for Postgres"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = object.__new__(cls)
            db_config = {'dbname': PG_DB, 'host': PG_HOST,
                     'password': PG_PASS, 'port': PG_PORT, 'user': PG_USER}
            try:
                print('connecting to PostgreSQL database...')
                connection = Postgres._instance.connection = psycopg2.connect(**db_config)
                cursor = Postgres._instance.cursor = connection.cursor()
                cursor.execute('SELECT VERSION()')
                db_version = cursor.fetchone()

            except Exception as error:
                print('Error: connection not established {}'.format(error))
                Postgres._instance = None

            else:
                print('connection established\n{}'.format(db_version[0]))

        return cls._instance

    def __init__(self):
        self.connection = self._instance.connection
        self.cursor = self._instance.cursor

    def query(self, query):
        try:
            result = self.cursor.execute(query)
        except Exception as error:
            print('error execting query "{}", error: {}'.format(query, error))
            return None
        else:
            return result

    def __del__(self):
        self.connection.close()
        self.cursor.close()
        


pgSecret = ("postgresql://postgres:{}@localhost:{}".format(PG_PASS, PG_PORT))

secret_key = '55823c2e-b31b-4eaf-a44b-025c7fbb1645'

