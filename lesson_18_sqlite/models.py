from database import get_connection


def create_user(username: str, email: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, email) VALUES (?, ?);",
        (username, email)
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def create_issue(title: str, issue_type: str, priority: str, user_id: int, description: str = "", deadline: str = None) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO issues (title, description, issue_type, priority, status, deadline, user_id)
        VALUES (?, ?, ?, ?, 'Open', ?, ?);
        """,
        (title, description, issue_type, priority, deadline, user_id)
    )
    conn.commit()
    issue_id = cursor.lastrowid
    conn.close()
    return issue_id


def get_all_issues() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM issues;")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def get_issues_with_usernames() -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT issues.id, issues.title, issues.issue_type, issues.priority, issues.status, users.username
        FROM issues
        LEFT JOIN users ON issues.user_id = users.id;
    """)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]


def update_issue_status(issue_id: int, new_status: str) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE issues SET status = ? WHERE id = ?;",
        (new_status, issue_id)
    )
    conn.commit()
    updated = cursor.rowcount > 0
    conn.close()
    return updated


def delete_issue(issue_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM issues WHERE id = ?;", (issue_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def add_comment(issue_id: int, author_id: int, text: str) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO comments (issue_id, author_id, text) VALUES (?, ?, ?);",
        (issue_id, author_id, text)
    )
    conn.commit()
    comment_id = cursor.lastrowid
    conn.close()
    return comment_id


def get_issue_with_comments(issue_id: int) -> dict:
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT issues.id, issues.title, issues.issue_type, issues.priority, issues.status, users.username AS author
        FROM issues
        LEFT JOIN users ON issues.user_id = users.id
        WHERE issues.id = ?;
    """, (issue_id,))
    issue_row = cursor.fetchone()

    if not issue_row:
        conn.close()
        return {}

    issue_data = dict(issue_row)

    cursor.execute("""
        SELECT comments.id, comments.text, users.username AS author
        FROM comments
        JOIN users ON comments.author_id = users.id
        WHERE comments.issue_id = ?;
    """, (issue_id,))
    comments_rows = cursor.fetchall()
    conn.close()

    issue_data["comments"] = [dict(c) for c in comments_rows]
    return issue_data