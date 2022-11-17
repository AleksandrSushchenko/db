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

def change_client(conn, name, first_name=None, email=None, phones=None):
    with conn.cursor() as cur:
        cur.execute("""
        select name from user_guide where name=%s  
        """, (name,))

        client_name = cur.fetchone()

        if client_name == None:
            print('Пользователя с таким именем несуществует!')
        else:
            user_name = client_name[0]
            if first_name is not None:
                cur.execute("""
                update user_guide set firstname = %s where name = %s
                """, (first_name, user_name,))
                print(f'Фамиля у {user_name} изменена')
            if email is not None:
                cur.execute("""
                update user_guide set email = %s where name = %s
                """,(email, user_name,))
                print(f'Почта у {user_name} изменена')
            if phones is not None:
                cur.execute("""
                select id from user_guide where name=%s
                """, (name,))

                client_id = cur.fetchone()
                user_id = client_id[0]

                cur.execute("""
                update tel set tel = %s where id_user =%s
                 """, (phones, user_id,))
                print(f'Телефон у {user_name} изменен')
    conn.commit()

def delete_phone(conn, id_user, tel):
    with conn.cursor() as cur:
        cur.execute("""
        delete from tel where id_user=%s and tel = %s
        """, (id_user, tel))
    conn.commit()

def delete_client(conn, client_id):
    with conn.cursor() as cur:
        cur.execute("""
        delete from tel where id_user=%s
        """, (client_id,))

        cur.execute("""
        delete from user_guide where id=%s
        """, (client_id,))
    conn.commit()


def find_client(conn, name=None, first_name=None, email=None, phone=None):
    with conn.cursor() as cur:
        cur.execute("""
        select user_guide, tel 
        from user_guide join tel
        on user_guide.name  = %s  or user_guide.firstname = %s or user_guide.email = %s or tel.tel = %s
        group by user_guide.id, tel.tel 
        """, (name, first_name, email, phone,))
        print(cur.fetchall())
    conn.commit()

with psycopg2.connect(database="guide", user="postgres", password="1109") as conn:
    create_db(conn)
    add_client(conn, 'Alex', 'sokolov', '1@gmail.com', '7-962-264-0202')
    add_client(conn, 'Petr', 'sokolov', '2gmail.com', '8-666-698-8827')
    add_client(conn, 'Ivan', 'Petrov', '3gmail.com', '8-466-668-1484')
    add_tel(conn, 2, '8-211-444-4444')
    change_client(conn, 'Ivan', 'IVANOV', '33333333@mail.com', '8-888-888-8888')
    change_client(conn, 'Petr', 'Petrov')
    delete_phone(conn, '3', '8-888-888-8888')
    delete_client(conn, '1')
    find_client(conn, 'Petr')


conn.close()




