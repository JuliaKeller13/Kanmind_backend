def build_auth_response(user, token):
    return {
        "token": token,
        "fullname": user.fullname,
        "email": user.email,
        "user_id": user.id,
    }