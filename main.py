from flask import Flask, session
from flask_session import Session
from app.routes import routes
from app.database import init_db
from flask import Flask
import os

template_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), "app", "templates")
app = Flask(__name__, template_folder=template_dir)

app = Flask(__name__)
app.secret_key = "roza-database"
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
app.register_blueprint(routes)

init_db()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
