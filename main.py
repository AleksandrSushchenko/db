import psycopg2

def create_db(conn):
    with conn.cursor() as cur:
        cur.execute("""
        DROP TABLE "tel";
        DROP TABLE "user_guide";
        """)

        cur.execute("""
            CREATE TABLE IF NOT EXISTS user_guide(
            "id" int generated always as identity (increment 1 start 1 minvalue 1 maxvalue 2147483647 cache 1) PRIMARY KEY,
            "name" varchar(80) NOT NULL,
            firstname varchar(80) NOT NULL,
            "email" varchar(80) NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS "tel"(
            "id_tel" int generated always as identity (increment 1 start 1 minvalue 1 maxvalue 2147483647 cache 1) PRIMARY KEY,
            "tel" int,
            "id_user" int REFERENCES user_guide(id) 
            );
        """)
    conn.commit()


def change_client(conn, name, first_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO user_guide (name, firstname, email)
        VALUES (%s, %s, $s)
        """, (name,first_name,email,))
    conn.commit()


def add_phone(conn, client_id, phone):
    pass

def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass


with psycopg2.connect(database="guide", user="postgres", password="1109") as conn:
    create_db(conn)
    change_client(conn, 'Petr', 'Ivanov', '1@gmail.com')



conn.close()




