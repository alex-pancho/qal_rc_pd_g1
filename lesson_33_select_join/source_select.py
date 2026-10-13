from db_connector import get_connection

chek_conn = "SELECT current_database(), current_user;"


with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute(chek_conn)
        print(cursor.fetchall())
    conn.commit()