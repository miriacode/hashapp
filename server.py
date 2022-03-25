from flask_app import app

from flask_app.controllers import usersController
from flask_app.controllers import postsController

if __name__=="__main__":
    app.run(debug=True)