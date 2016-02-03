import os
from app import create_app
from flask.ext.script import Server, Manager

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
manager.add_command("runserver", Server(host="0.0.0.0", port=8000))

if __name__ == '__main__':
    manager.run()
