"""
General App package.
"""

from flask import Flask
import routing

app = Flask(__name__)

# Start frontend
if __name__ == "__main__":
    app.secret_key = "test"
    app.register_blueprint(routing.bp)
    app.run(debug=True)
