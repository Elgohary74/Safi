from app.models import NotificationSchema
from app.repositories.notification_repo import NotificationRepository


def test_persistence_repro():
    repo = NotificationRepository()

    # Create a dummy notification
    notif = NotificationSchema(
        message="Test persistence", user_id="test_user_123", type="generic"
    )

    # Add to DB
    notif_id = repo.add(notif)
    print(f"Created notification: {notif_id}")

    # Verify initial state
    fetched = repo.get_by_id(notif_id)
    assert fetched.is_read is False, "Should differ from default?"
    # default is False.

    # Mark as read
    repo.mark_as_read(notif_id)

    # Verify updated state
    fetched_again = repo.get_by_id(notif_id)

    if fetched_again.is_read:
        print("SUCCESS: Notification marked as read persisted.")
    else:
        print("FAILURE: Notification is still unread.")

    # Clean up
    repo.delete(notif_id)


if __name__ == "__main__":
    test_persistence_repro()
