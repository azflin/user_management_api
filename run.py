import argparse

from user_management_api import app, db

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--create_database', action='store_true')
    args = parser.parse_args()

    if args.create_database:
        db.drop_all()
        db.create_all()
    else:
        app.run(debug=True)
