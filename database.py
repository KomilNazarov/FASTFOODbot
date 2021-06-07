import sqlite3

__connection = None


def get_connect():
    global __connection
    if __connection is None:
        __connection = sqlite3.connect("savat.db")
    return  __connection

def create_base(force: bool = False):
    conn = get_connect()
    b = conn.cursor()

    if force:
        b.execute("DROP TABLE IF EXISTS user_product")

    b.execute("""
              CREATE TABLE IF NOT EXISTS user_product(
              id INTEGER PRIMARY KEY ,
              user_id INTEGER NOT NULL, 
              products VARCHAR )""")
    conn.commit()

def add_message(user_id = int , products = str):
    conn = get_connect()
    b = conn.cursor()
    b.execute("INSERT INTO user_product (user_id , products) VALUES ( ? , ?)" , (user_id , products))
    conn.commit()


if __name__ ==  '__main__':
    create_base()

    add_message(user_id=123 , products="daxxuya olma")









