import os
from dotenv import load_dotenv
import psycopg2
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask
from main import db  # Replace with your actual app module name
from main import Cafe  # Replace with your actual model import

load_dotenv()
# Create a minimal Flask app context (needed for SQLAlchemy models)
app = Flask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI=os.environ.get("DB_URI"),  # Your local SQLite path
    SQLALCHEMY_TRACK_MODIFICATIONS=False
)
db.init_app(app)


def migrate_data():
    with app.app_context():
        # PostgreSQL connection string from Render
        postgres_uri = os.environ.get("POSTGRES_DB_URI")  # Replace with your actual connection string

        # Create engine for PostgreSQL
        postgres_engine = create_engine(postgres_uri)
        PostgresSession = sessionmaker(bind=postgres_engine)
        postgres_session = PostgresSession()

        # Get all cafes from SQLite (using Flask-SQLAlchemy)
        cafes = Cafe.query.all()
        print(f"Found {len(cafes)} cafes in SQLite database")

        # Insert into PostgreSQL
        for cafe in cafes:
            print(f"Migrating cafe: {cafe.name}")
            # Create a new cafe object for PostgreSQL
            new_cafe = Cafe(
                name=cafe.name,
                map_url=cafe.map_url,
                img_url=cafe.img_url,
                location=cafe.location,
                seats=cafe.seats,
                has_toilet=cafe.has_toilet,
                has_wifi=cafe.has_wifi,
                has_sockets=cafe.has_sockets,
                can_take_calls=cafe.can_take_calls,
                coffee_price=cafe.coffee_price
                # Add any other fields your model has
            )
            postgres_session.add(new_cafe)

        # Commit the changes
        try:
            postgres_session.commit()
            print("Migration completed successfully!")
        except Exception as e:
            postgres_session.rollback()
            print(f"Error during migration: {e}")
        finally:
            postgres_session.close()


if __name__ == "__main__":
    migrate_data()