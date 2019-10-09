from decouple import config
from dotenv import load_dotenv
from flask import Flask, render_template, request
from .model import DB, User
from .twitter import add_or_update_user
from .predict import predict_user

load_dotenv()

def create_app():
    """Create and configure an instance of the Flask application"""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config('DATABASE_URL')
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template('base.html', title='TwitOff', users=User.query.all())

    @app.route('/user', methods=['POST'])
    @app.route('/user/<name>', methods=['GET'])
    def user(name=None, message=''):
        name = name or request.values['user_name']
        try:
            if request.method == 'POST':
                add_or_update_user(name)
                message = "User {} successfully added!".format(name)
            tweets = User.query.filter(User.username == name).one().tweets
        except Exception as e:
            message = 'Error adding {}: {}'.format(name, e)
            tweets = []
        return render_template('user.html', title=name, tweets=tweets, message=message)

    @app.route('/compare', methods=['POST'])
    def compare(message=''):
        user1 = request.values['user1']
        user2 = request.values['user2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = 'cannot compare a user to themselves!'
        else:
            prediction = predict_user(user1,user2,tweet_text)
            message = '"{}" is more likely to said by {} than {}'.format(tweet_text,
            user1 if prediction else user2,user2 if prediction else user2)
        return render_template('prediction.html',message=message)


    return app