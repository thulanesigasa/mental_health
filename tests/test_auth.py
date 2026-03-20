import pytest
from app.models.user import User
from app.utils.security import hash_password

def test_login_successful(client, init_database):
    user = User.query.filter_by(email='test@example.com').first()
    user.password_hash = hash_password('TestSecure123!')
    init_database.session.commit()
    
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'TestSecure123!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Logged in successfully' in response.data

def test_login_failure(client, init_database):
    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'WrongPassword123'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Invalid email or password' in response.data

def test_register_successful(client, init_database):
    response = client.post('/auth/register', data={
        'email': 'newuser@example.com',
        'password': 'NewUser123!'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Registration successful' in response.data
    
    new_user = User.query.filter_by(email='newuser@example.com').first()
    assert new_user is not None

def test_admin_access_allowed(client, init_database):
    admin = User.query.filter_by(email='admin@example.com').first()
    admin.password_hash = hash_password('AdminSec123!')
    init_database.session.commit()
    
    client.post('/auth/login', data={'email': 'admin@example.com', 'password': 'AdminSec123!'})
    response = client.get('/admin/dashboard', follow_redirects=True)
    
    assert response.status_code == 200
    # Because of the dark theme styling and RBAC, we ensure "Admin" is present on the layout
    assert b'Admin' in response.data

def test_admin_access_denied_for_regular_user(client, init_database):
    user = User.query.filter_by(email='test@example.com').first()
    user.password_hash = hash_password('TestSecure123!')
    init_database.session.commit()
    
    client.post('/auth/login', data={'email': 'test@example.com', 'password': 'TestSecure123!'})
    response = client.get('/admin/dashboard', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Action forbidden' in response.data
