import json
from functools import wraps

from flask import Blueprint, render_template, request

main_routes = Blueprint("main_routes", __name__, template_folder="../templates")


def authenticate(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.cookies.get("user")
        if auth is None or auth == "null" or auth == "undefined":
            return render_template('login.html')
        return f(*args, **kwargs)
    return wrapper


@main_routes.route('/')
def main():
    cookies = request.cookies
    user = cookies.get("user")
    return render_template('index.html', user=json.loads(str(user)))


@main_routes.route('/dashboard')
@authenticate
def dashboard():
    cookies = request.cookies
    user = cookies.get("user")
    return render_template('index.html', user=json.loads(str(user)))


@main_routes.route('/workflow')
@authenticate
def workflow():
    cookies = request.cookies
    user = cookies.get("user")
    return render_template('workflow.html', user=json.loads(str(user)))


@main_routes.route('/devices')
@authenticate
def devices():
    cookies = request.cookies
    user = cookies.get("user")
    return render_template('devices.html', user=json.loads(str(user)))
