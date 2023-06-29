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
            

#db = Database(user, password, db, host)

#db_conn = db.connect()
#query = "INSERT INTO users (id, name) VALUES (9, 'stacy') RETURNING id"
#if db_conn:
#    try:
#        result = db.query_db(query, db_conn)
#        print(result)
#    except:
#        print("Incorrect query")
        
    
#else:
#    print("Error has ocurred while connecting to database")
