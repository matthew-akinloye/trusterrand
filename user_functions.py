from flask import session, request

from models import User


def check_user():
    """
    This function will check session and cookies for active login
    :return: User or None
    """
    if 'email' in session and 'id' in session:
        active_user = User.query.filter(User.id == session['id']).first()
        return active_user
    else:
        user_id = request.cookies.get('user_id')
        pw = request.cookies.get('pw')
        active_user = User.query.filter(
            User.id == user_id).filter(
            User.password_hash == pw
        ).first()
        return active_user
