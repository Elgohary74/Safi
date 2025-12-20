from app.models.user import UserRegister
from app.repositories.notification_repo import NotificationRepository
from app.services import AuthService


def _register_and_login(client, name="notifyuser", email="notify@example.com"):
    AuthService().register_user(
        UserRegister(name=name, email=email, password="ValidPass9!")
    )
    resp = client.post(
        "/auth/login",
        data={"email": email, "password": "ValidPass9!"},
        follow_redirects=False,
    )
    assert resp.status_code == 302


def test_get_notifications_returns_unread_for_user(client):
    repo = NotificationRepository()
    repo.collection.delete_many({})

    # Register/login a user
    email = "notify1@example.com"
    _register_and_login(client, name="Notify One", email=email)
    user = AuthService().user_repo.get_by_email(email)

    # Seed two unread notifications for the user
    from app.models.notification import NotificationSchema

    repo.add(NotificationSchema(user_id=user.user_id, message="Test 1"))
    repo.add(NotificationSchema(user_id=user.user_id, message="Test 2"))

    r = client.get("/notifications/")
    assert r.status_code == 200
    data = r.get_json()
    assert isinstance(data, list)
    assert len(data) == 2
    assert {"message", "notification_id", "timestamp", "type"}.issubset(
        set(data[0].keys())
    )


def test_mark_as_read_marks_notification_and_redirects(client):
    repo = NotificationRepository()
    repo.collection.delete_many({})

    email = "notify2@example.com"
    _register_and_login(client, name="Notify Two", email=email)
    user = AuthService().user_repo.get_by_email(email)

    from app.models.notification import NotificationSchema

    notif_id = repo.add(
        NotificationSchema(user_id=user.user_id, message="Mark me read")
    )

    r = client.post(
        f"/notifications/{notif_id}/mark_as_read",
        follow_redirects=False,
    )

    # Should redirect to activity page
    assert r.status_code == 302
    assert "/dashboard/activity" in r.headers.get("Location", "")

    # Now unread list should be empty
    unread = repo.get_unread_by_user(user.user_id)
    assert len(unread) == 0
