from flask import Flask

app = Flask(__name__)

from routing import *
from deck_manager import *

# Start frontend
if __name__ == "__main__":
    app.secret_key = "test"
    app.run(debug=True)
