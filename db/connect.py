import psycopg2

from misc import user, password, db, host

class Database:
    def __init__(self, user=user, password=password, db=db, host=host):
        self.user = user
        self.password = password
        self.db = db
        self.host = host

    def connect(self):
        try:
            conn = psycopg2.connect(dbname=self.db, user=self.user, password=self.password, host=self.host)
            return conn
        except:
            return None

    @staticmethod
    def query_db(query, conn):
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return result

db = Database(user, password, db, host)

db_conn = db.connect()
query = "SELECT * FROM users"
if db_conn:
    try:
        result = db.query_db(query, db_conn)
        print(result)
    except Exception as _er:
        print("Incorrect query: ", _er)
else:
    print("Error has ocurred while connecting to database")


