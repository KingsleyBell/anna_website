# Import routes
from routes import main
from routes import admin
from routes import ajax
from util import application


if __name__ == "__main__":
    application.run(host='0.0.0.0', port=800)
