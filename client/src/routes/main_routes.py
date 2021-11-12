import requests
from flask import Blueprint, render_template

main_routes = Blueprint("main_routes", __name__, template_folder="../templates")

@main_routes.route('/')
def dashboard():
    return render_template('index.html')


@main_routes.route('/workflow')
def workflow():
    return render_template('workflow.html')


@main_routes.route('/devices')
def devices():
    onus_ubiquiti = requests.get("http://ac-vision:8000/api/v1.0/ressources/ubiquiti/onus").json()
    olt_ubiquiti = requests.get("http://ac-vision:8000/api/v1.0/ressources/ubiquiti/olt").json()
    return render_template('devices.html', onus_ubiquiti=onus_ubiquiti, olt_ubiquiti=olt_ubiquiti)