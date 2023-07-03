import psycopg2
from db.misc import user, password, db, host

class Database:
    user = user
    password = password
    db = db
    host = host

    def connect(self):
        try:
            with psycopg2.connect(dbname=self.db, user=self.user, password=self.password, host=self.host) as conn:
                return conn
        except:
            return None
        
    @staticmethod
    def query_db(query, conn):
        with conn.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchall()
                conn.commit()
                conn.close()
                return result
            


