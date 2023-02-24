import os
from dotenv import load_dotenv
basedir= os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config():
    FLASK_APP= os.getenv('FLASK_APP')
    FLASK_ENV= os.getenv('FLASK_ENV')
    SECRET_KEY= os.environ.get('SECRET_KEY') or 'Jaal'
    SQLALCHEMY_DATABASE_URI= os.environ.get('DATABASE_URI') or 'sqlite://' + os.path.join(basedir, 'app.db')
    #if the above line fails add another / to the sqlite
    SQLALCHEMY_TRACK_NOTIFICATIONS= False
