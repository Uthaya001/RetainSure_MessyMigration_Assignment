import re

def sanitize_input(data):
    """Sanitize input data to prevent injection attacks"""
    if isinstance(data, str):
        dangerous_patterns = [';', '--', '/*', '*/', 'xp_', 'sp_']
        sanitized = data
        for pattern in dangerous_patterns:
            sanitized = sanitized.replace(pattern, '')
        return sanitized.strip()
    return data

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Validate password strength"""
    if not password:
        return False, "Password is required"
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    if not re.search(r'[A-Za-z]', password):
        return False, "Password must contain at least one letter"
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    return True, "Password is valid"

def validate_name(name):
    """Validate user name"""
    if not name:
        return False, "Name is required"
    if len(name.strip()) < 2:
        return False, "Name must be at least 2 characters long"
    if len(name.strip()) > 100:
        return False, "Name must be less than 100 characters"
    if not re.match(r'^[a-zA-Z\s\'\-\.]+$', name.strip()):
        return False, "Name contains invalid characters"
    return True, "Name is valid"

def validate_user_data(data, partial=False):
    """
    Validates user data for creation or update.

    Args:
        data (dict): incoming JSON data
        partial (bool): True if for update (allows missing fields)

    Returns:
        dict: { "valid": bool, "message": str }
    """
    if not data:
        return {"valid": False, "message": "No data provided"}

    # Auto-strip keys and string values
    cleaned_data = {}
    for k, v in data.items():
        key = k.strip()
        value = v.strip() if isinstance(v, str) else v
        cleaned_data[key] = value

    errors = []

    # Validate name
    if 'name' in cleaned_data:
        valid, msg = validate_name(cleaned_data['name'])
        if not valid:
            errors.append(msg)
        else:
            cleaned_data['name'] = sanitize_input(cleaned_data['name'])
    elif not partial:
        errors.append("Name is required")

    # Validate email
    if 'email' in cleaned_data:
        if not validate_email(cleaned_data['email']):
            errors.append("Invalid email format")
        else:
            cleaned_data['email'] = sanitize_input(cleaned_data['email']).lower()
    elif not partial:
        errors.append("Email is required")

    # Validate password
    if 'password' in cleaned_data:
        valid, msg = validate_password(cleaned_data['password'])
        if not valid:
            errors.append(msg)
    elif not partial:
        errors.append("Password is required")

    # Only check for unexpected fields if it's not partial update
    allowed_fields = {'name', 'email', 'password'}
    extra_fields = set(cleaned_data.keys()) - allowed_fields
    if extra_fields:
        errors.append(f"Unexpected fields: {', '.join(extra_fields)}")

    if errors:
        return {"valid": False, "message": "; ".join(errors)}

    return {"valid": True, "message": "Validation passed"}
def validate_login_data(data):
    """Validate login request payload"""
    if not data:
        return {"valid": False, "message": "No data provided"}

    errors = []

    if 'email' not in data or not data['email']:
        errors.append("Email is required")
    elif not validate_email(data['email']):
        errors.append("Invalid email format")

    if 'password' not in data or not data['password']:
        errors.append("Password is required")

    # Optional: check for unexpected fields
    allowed_fields = {'email', 'password'}
    unexpected_fields = set(data.keys()) - allowed_fields
    if unexpected_fields:
        errors.append(f"Unexpected fields: {', '.join(unexpected_fields)}")

    if errors:
        return {"valid": False, "message": "; ".join(errors)}

    return {"valid": True, "message": "Login data is valid"}
