from flask import url_for, redirect, session
from functools import wraps


def is_login(func):
    @wraps(func)
    def check_login(*args, **kwargs):
        user = session.get('user')
        if user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('index'))
    return check_login