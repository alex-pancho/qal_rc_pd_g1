from db_connector import get_connection

insert_user = """
insert into users 
(name, email)
values ('Alex2', 'email@gmail.com');
"""
select_user = """
select * from users;
"""


with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute(select_user)
        print(cursor.fetchall())
    conn.commit()
