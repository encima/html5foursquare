from Flask import Flask
from flask.ext.social import Social
from flask.ext.social.datastore import SQLAlchemyConnectionDatastore
import config

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SOCIAL_FOURSQUARE'] = {
	'consumer_key': config.SQ_CLIENT_ID,
    'consumer_secret': config.SQ_CLIENT_SECRET
}


