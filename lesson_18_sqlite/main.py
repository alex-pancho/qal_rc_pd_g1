from database import init_db
import models


def main():
    init_db()

    alice_id = models.create_user("alice", "alice@example.com")
    bob_id = models.create_user("bob", "bob@example.com")

    issue1_id = models.create_issue("Fix login bug", "Bug", "High", alice_id)
    issue2_id = models.create_issue("Write unit tests", "Task", "Medium", bob_id)
    issue3_id = models.create_issue("Update README", "Task", "Low", alice_id)

    models.update_issue_status(issue3_id, "Done")

    models.add_comment(issue1_id, bob_id, "I can reproduce this bug on Chrome.")
    models.add_comment(issue2_id, alice_id, "Will add tests for auth module.")

    issues = models.get_issues_with_usernames()
    for item in issues:
        print(f"[{item['id']}] {item['title']} | {item['issue_type']} | {item['priority']} | {item['status']} | {item['username']}")

    print("\n--- Бонус: Задача з коментарями ---")
    issue_details = models.get_issue_with_comments(issue1_id)
    print(f"Задача: {issue_details['title']} (Автор: {issue_details['author']})")
    print("Коментарі:")
    for comment in issue_details["comments"]:
        print(f" - {comment['author']}: {comment['text']}")


if __name__ == "__main__":
    main()