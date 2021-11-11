from flask import Blueprint

main_routes = Blueprint("main_routes", __name__, template_folder="../templates")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/workflow')
def workflow():
    return render_template('workflow.html')


@app.route('/devices')
def devices():
    onus_ubiquiti = getUbiquitiOnusDetails()
    olt_ubiquiti = getUbiquitiOltDetails()
    return render_template('devices.html', onus_ubiquiti=onus_ubiquiti, olt_ubiquiti=olt_ubiquiti)