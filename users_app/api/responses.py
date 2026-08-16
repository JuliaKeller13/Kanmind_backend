def build_auth_response(user, token):
    """Build the shared authentication response payload."""
    return {
        "token": token,
        "fullname": user.fullname,
        "email": user.email,
        "user_id": user.id,
    }