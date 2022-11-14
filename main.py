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
    pass


def add_phone(conn, client_id, phone):
    pass

def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass

def add_client(conn, name, first_name, email, tel: int):
    with conn.cursor() as cur:
        cur.execute("""
        insert into user_guide (name, firstname, email)
        values (%s, %s, %s) returning id
        """, (name, first_name, email,))
        id_client = cur.fetchone()
        id_user = int(id_client[0])

        cur.execute("""
        insert into tel (tel, id_user)
        values (%s, %s)
        """ (tel, id_user, ))

    conn.commit()



with psycopg2.connect(database="guide", user="postgres", password="1109") as conn:
    create_db(conn)

    add_client(conn, 'Alex', 'sokolov', '1@gmail.com', 444444)
    add_client(conn, 'Petr', 'sokolov', '2gmail.com', 988827)
    add_client(conn, 'Ivan', 'Petrov', '3gmail.com', 8484848484)

    # name = 'Petr'
    # first_name = 'Ivanov'
    # email = '1@gmail.com'
    # with conn.cursor() as cur:
    #     cur.execute("""
    #     insert into user_guide (name, firstname, email)
    #     values (%s, %s, %s)
    #     """, (name, first_name, email))
    # conn.commit()




conn.close()




