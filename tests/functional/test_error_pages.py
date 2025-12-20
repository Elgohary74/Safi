import pytest
from app.utils.exceptions import ResourceNotFound

def test_app_error_renders_html(client):
    # We can try to access a non-existent group's members to trigger ResourceNotFound
    # But we need to be logged in probably, depending on the route protection.
    # Actually, let's look at group_controller.py, get_group_members is not protected by @jwt_required in the snippet I saw?
    # Wait, BaseController might have it?
    # Let's just try to hit a known route that raises ResourceNotFound.
    
    # Or we can registering a temporary route in the test
    
    # Let's try to hit /groups/nonexistent/members
    # But wait, we need to handle authentication if it's required.
    # GroupController inherits BaseController.
    
    # Let's rely on the fact that we can mock the service to raise the exception, 
    # OR simpler: just assume authentication is needed and provide it, or find a public route?
    # Most routes require auth.
    
    # Let's try a simple approach: define a route in the app fixture that raises AppError?
    # But we are using the 'client' fixture which uses 'app' fixture from conftest.
    
    from flask import Flask
    from app.utils.exceptions import AppError
    
    # We can't easily modify the running app fixture here without affecting others if scope is session?
    # The 'client' fixture is function scoped but 'app' is session scoped.
    
    # Let's just Authenticate and then hit a route we know raises an exception.
    # /groups/<group_id>/members raises ResourceNotFound if group is None.
    
    # Register/Login
    from app.services import AuthService
    from app.models.user import UserRegister
    email = "error_test@example.com"
    AuthService().register_user(
        UserRegister(name="Error User", email=email, password="Password123!")
    )
    client.post(
        "/auth/auth-controller/login",
        data={"email": email, "password": "Password123!"},
    )
    
    # Hit /groups/nonresident_id/members
    resp = client.get("/groups/nonexistent_id/members")
    
    # It should be 404 status
    assert resp.status_code == 404
    
    # It should be HTML
    assert "text/html" in resp.content_type
    
    # It should contain content from error.html
    # e.g. "Error 404" or "Resource not found"
    text = resp.get_data(as_text=True)
    assert "Error 404" in text
    assert "Resource not found" in text
