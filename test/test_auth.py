import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_register_and_login(client):
    register_url = reverse('register')
    login_url = reverse('token_obtain_pair')

    payload = {
        'email': 'user@test.com',
        'password': 'testpassword123',
    }

    response = client.post(register_url, payload, content_type='application/json')
    assert response.status_code == 201
    body = response.json()
    assert body['success'] is True
    assert body['data']['email'] == payload['email']

    response = client.post(login_url, payload, content_type='application/json')
    assert response.status_code == 200
    tokens = response.json()
    assert 'access' in tokens and 'refresh' in tokens


@pytest.mark.django_db
def test_registration_login_and_password_reset(client):
    register_url = reverse('register')
    login_url = reverse('token_obtain_pair')
    forgot_password_url = reverse('forgot_password')
    reset_password_url = reverse('reset_password')

    # Test 1: Registration
    register_payload = {
        'email': 'reset_test@test.com',
        'password': 'strongpassword123',
        'full_name': 'Test User'
    }

    response = client.post(register_url, register_payload, content_type='application/json')
    assert response.status_code == 201
    body = response.json()
    assert body['success'] is True
    assert body['data']['email'] == register_payload['email']
    assert body['data']['full_name'] == register_payload['full_name']

    # Test 2: Login
    login_payload = {
        'email': 'reset_test@test.com',
        'password': 'strongpassword123',
    }

    response = client.post(login_url, login_payload, content_type='application/json')
    assert response.status_code == 200
    tokens = response.json()
    assert 'access' in tokens and 'refresh' in tokens

    # Test 3: Forgot Password
    forgot_payload = {
        'email': 'reset_test@test.com'
    }

    response = client.post(forgot_password_url, forgot_payload, content_type='application/json')
    assert response.status_code == 200
    body = response.json()
    assert body['success'] is True
    assert 'token' in body

    reset_token = body['token']

    # Test 4: Reset Password
    reset_payload = {
        'token': reset_token,
        'password': 'newpassword123'
    }

    response = client.post(reset_password_url, reset_payload, content_type='application/json')
    assert response.status_code == 200
    body = response.json()
    assert body['success'] is True

    # Test 5: Login with new password
    new_login_payload = {
        'email': 'reset_test@test.com',
        'password': 'newpassword123',
    }

    response = client.post(login_url, new_login_payload, content_type='application/json')
    assert response.status_code == 200
    tokens = response.json()
    assert 'access' in tokens and 'refresh' in tokens

    # Test 6: Old password should not work
    old_login_payload = {
        'email': 'reset_test@test.com',
        'password': 'strongpassword123',
    }

    response = client.post(login_url, old_login_payload, content_type='application/json')
    assert response.status_code == 401  # Unauthorized with old password


@pytest.mark.django_db
def test_profile_endpoint_authentication(client):
    register_url = reverse('register')
    login_url = reverse('token_obtain_pair')
    profile_url = reverse('profile')

    # Test 1: Register a user
    register_payload = {
        'email': 'profile_test@test.com',
        'password': 'testpassword123',
        'full_name': 'Profile Test User'
    }

    response = client.post(register_url, register_payload, content_type='application/json')
    assert response.status_code == 201

    # Test 2: Login to get token
    login_payload = {
        'email': 'profile_test@test.com',
        'password': 'testpassword123',
    }

    response = client.post(login_url, login_payload, content_type='application/json')
    assert response.status_code == 200
    tokens = response.json()
    access_token = tokens['access']

    # Test 3: Profile endpoint without authentication should fail
    response = client.get(profile_url)
    assert response.status_code == 401
    assert 'Authentication credentials were not provided' in response.json()['detail']

    # Test 4: Profile endpoint with authentication should succeed
    headers = {'HTTP_AUTHORIZATION': f'Bearer {access_token}'}
    response = client.get(profile_url, **headers)
    assert response.status_code == 200
    profile_data = response.json()
    assert profile_data['email'] == 'profile_test@test.com'
    assert profile_data['full_name'] == 'Profile Test User'
    assert 'id' in profile_data


@pytest.mark.django_db
def test_invalid_password_reset_token(client):
    reset_password_url = reverse('reset_password')

    # Test with invalid token
    reset_payload = {
        'token': 'invalid_token_123',
        'password': 'newpassword123'
    }

    response = client.post(reset_password_url, reset_payload, content_type='application/json')
    assert response.status_code == 400
    assert 'Invalid or expired token' in response.json()['detail']


@pytest.mark.django_db
def test_forgot_password_nonexistent_user(client):
    forgot_password_url = reverse('forgot_password')

    # Test with non-existent email
    forgot_payload = {
        'email': 'nonexistent@test.com'
    }

    response = client.post(forgot_password_url, forgot_payload, content_type='application/json')
    assert response.status_code == 200
    body = response.json()
    assert body['success'] is False


