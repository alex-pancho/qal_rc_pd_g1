from db_connector import get_connection

aggr_01 = """
SELECT
    COUNT(*)               AS total,
    COUNT(score)           AS graded,
    SUM(score)             AS total_score,
    ROUND(AVG(score), 2)   AS avg_score,
    MIN(score)             AS min_score,
    MAX(score)             AS max_score
FROM submissions;
"""

with get_connection() as conn:
    with conn.cursor() as cursor:
        cursor.execute(aggr_01)
        print(cursor.fetchall())
    conn.commit()
