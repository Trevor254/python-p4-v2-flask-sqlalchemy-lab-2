from flask import Flask
from flask_migrate import Migrate
from models import db

def create_app():
    """Application factory function to create Flask app instance."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    @app.route('/')
    def index():
        return '<h1>Flask SQLAlchemy Lab 2</h1>'

    return app  # ✅ Return app instance

# Create the app instance (used in production)
app = create_app()

if __name__ == '__main__':
    app.run(port=5555, debug=True)