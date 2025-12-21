import os
import sys
from datetime import datetime

from flask import Flask, render_template

# Add the project root to the python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))

app = Flask(__name__, template_folder="../app/templates", static_folder="../app/static")


# Mock current_user
class MockUser:
    user_id = "test_user"
    name = "Test User"
    user_picture = None
    payment_methods = []


# Mock functions used in base.html
@app.context_processor
def inject_user():
    return dict(current_user=MockUser())


@app.route("/test_activity")
def test_activity():
    try:
        # We define a dummy user for the Notification model since it expects a User object in relationship but here we just need the schema or object with attributes
        # Actually Notification model requires user relationship which is SQLModel/SQLAlchemy.
        # For template rendering, we just need objects with attributes.
        # Let's mock the notification objects to avoid DB dependency.

        class MockNotification:
            def __init__(self, message, type, payload=None, is_read=False):
                self.notification_id = "123"
                self.message = message
                self.type = type
                self.payload = payload or {}
                self.timestamp = datetime.now()
                self.is_read = is_read

        mock_notifications = [
            MockNotification("Test Generic", "generic", is_read=False),
            MockNotification(
                "Test Invitation",
                "invitation",
                {"group_name": "Test'Trip"},
                is_read=True,
            ),
            MockNotification("Test Transaction", "transaction", is_read=False),
        ]

        # Function url_for mocks
        # We need to render the template
        with app.test_request_context():
            rendered = render_template(
                "activity.html",
                notifications=mock_notifications,
                current_user=MockUser(),
            )
            print("Template rendered successfully!")
            if "Test Generic" in rendered:
                print("Generic notification found.")
            if "Test Invitation" in rendered:
                print("Invitation notification found.")
            if "Test Trip" in rendered:
                print("Group name 'Test Trip' found in invitation.")
            if "Test Transaction" in rendered:
                print("Transaction notification found.")
            return rendered
    except Exception as e:
        print(f"Error rendering template: {e}")
        raise e


if __name__ == "__main__":
    test_activity()
