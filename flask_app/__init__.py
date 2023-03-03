from flask import Flask, render_template

app = Flask(__name__)

app.secret_key = "My secret key"

app.config['UPLOAD_FOLDER'] = 'flask_app/static/assets/images'

@app.route('/')
def home():
    return render_template('sign-in.html')

# https://www.youtube.com/watch?v=LC-14nHGaMY