def assert_status_ok(response, allowed=(200, 201)):
    assert response.status_code in allowed, response.text
