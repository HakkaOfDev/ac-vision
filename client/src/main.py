import uvicorn
from flask import Flask

from routes.main_routes import main_routes
from routes.user_routes import user_routes

app = Flask(__name__)
app.register_blueprint(main_routes)
app.register_blueprint(user_routes)

if __name__ == '__main__':
    app.run()
