from flask import Flask

app = Flask(__name__)

app.secret_key = "My secret key"

app.config['UPLOAD_FOLDER'] = 'flask_app/static/assets/images'

# https://www.youtube.com/watch?v=LC-14nHGaMY