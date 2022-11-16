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
            "tel" varchar(20),
            "id_user" int REFERENCES user_guide(id) 
            );
        """)
    conn.commit()


def change_client(conn, name, first_name=None, email=None, phones=None):
    pass



def delete_phone(conn, client_id, phone):
    pass

def delete_client(conn, client_id):
    pass

def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    pass

def add_client(conn, name, first_name, email, tel):
    with conn.cursor() as cur:
        cur.execute("""
        insert into user_guide (name, firstname, email)
        values (%s, %s, %s) returning id
        """, (name, first_name, email,))
        id_client = cur.fetchone()
        id_user = id_client[0]
        cur.execute("""
        insert into tel (tel, id_user)
        values (%s, %s)
        """, (tel, id_user,))
    conn.commit()

def add_tel(conn, client_id, phone):
    with conn.cursor() as cur:
        cur.execute("""
        select id from user_guide where id = %s
        """, (client_id,))
        client_id = cur.fetchone()
        if client_id == None:
            print("Пользователя с таким id несуществует!")
        else:
            user_id = client_id[0]
            cur.execute("""
            insert into tel (tel, id_user)
            values (%s, %s)
            """, (phone, user_id,))
            print("Телефон добавлен")
    conn.commit()



with psycopg2.connect(database="guide", user="postgres", password="1109") as conn:
    create_db(conn)
    add_client(conn, 'Alex', 'sokolov', '1@gmail.com', '7-962-264-0202')
    add_client(conn, 'Petr', 'sokolov', '2gmail.com', '8-666-698-8827')
    add_client(conn, 'Ivan', 'Petrov', '3gmail.com', '8-466-668-1484')
    add_tel(conn, 2, '8-211-444-4444')
    add_tel(conn, 8, '8-211-333-4444')


conn.close()




