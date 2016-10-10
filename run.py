"""
Use run.py to run this application locally or to recreate the SQLite database.

Recreate SQLite database:
python run.py --create_database

Run webserver locally:
python run.py
"""
import argparse

from user_management_api import app, db

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--create_database', action='store_true', help="Recreate SQLite database.")
    args = parser.parse_args()

    if args.create_database:
        db.drop_all()
        db.create_all()
    else:
        app.run(debug=True)
