def assert_unauthorized(response):
    assert response.status_code == 401
    assert response.json["name"] == "Unauthorized"

def assert_redirect_login(response):
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/login")
