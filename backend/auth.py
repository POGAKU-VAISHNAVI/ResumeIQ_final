# auth.py — User authentication for ResumeIQ
import json, os, hashlib, uuid, time

# CRITICAL FIX: Store users.json in home directory alongside uploads.
# Writing to any path inside the project workspace triggers Live Server reload.
USERS_FILE = os.path.join(os.path.expanduser('~'), 'resumeiq_uploads', 'users.json')
TOKENS     = {}   # { token: email }  — in-memory, resets on restart

def _load():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        return json.load(open(USERS_FILE))
    except:
        return {}

def _save(users):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    json.dump(users, open(USERS_FILE, 'w'), indent=2)

def _hash(pw):
    return hashlib.sha256(pw.encode()).hexdigest()

def _token():
    return uuid.uuid4().hex + uuid.uuid4().hex

def signup(name, email, phone, password, confirm_password):
    if not name or not email or not password:
        return False, 'Name, email and password are required.', None
    if password != confirm_password:
        return False, 'Passwords do not match.', None
    if len(password) < 6:
        return False, 'Password must be at least 6 characters.', None
    users = _load()
    if email in users:
        return False, 'An account with this email already exists.', None
    users[email] = {
        'name': name, 'email': email, 'phone': phone,
        'password_hash': _hash(password), 'created': time.time()
    }
    _save(users)
    return True, 'Account created successfully!', {'name': name, 'email': email}

def login(identifier, password):
    users = _load()
    user  = None
    for u in users.values():
        if u['email'] == identifier or u.get('phone') == identifier:
            user = u
            break
    if not user:
        return False, 'No account found with these credentials.', None
    if user['password_hash'] != _hash(password):
        return False, 'Incorrect password. Please try again.', None
    token = _token()
    TOKENS[token] = user['email']
    return True, 'Login successful!', {'token': token, 'name': user['name'], 'email': user['email']}

def logout(token):
    if token and token in TOKENS:
        del TOKENS[token]
        return True, 'Logged out successfully.'
    return False, 'Invalid or expired session.'

def get_user_by_token(token):
    if not token or token not in TOKENS:
        return None
    email = TOKENS[token]
    return _load().get(email)

def update_profile(token, updates):
    user = get_user_by_token(token)
    if not user:
        return False, 'Unauthorized. Please login.'
    users = _load()
    allowed = ['name', 'phone', 'location', 'linkedin', 'github']
    for k in allowed:
        if k in updates and updates[k]:
            users[user['email']][k] = updates[k]
    _save(users)
    return True, 'Profile updated successfully!'

def reset_password(email, new_password, confirm_password):
    if not email or not new_password:
        return False, 'Email and new password are required.'
    if new_password != confirm_password:
        return False, 'Passwords do not match.'
    if len(new_password) < 6:
        return False, 'Password must be at least 6 characters.'
    users = _load()
    if email not in users:
        return False, 'No account found with this email.'
    users[email]['password_hash'] = _hash(new_password)
    _save(users)
    return True, 'Password reset successfully!'
