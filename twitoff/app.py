from flask import Flask,render_template
from .model import DB, User

def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/karthikmahendra/Desktop/Twitoff/db.sqlite3'
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html',title = 'the space jam!',users = User.query.all())

    return app


