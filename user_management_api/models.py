from user_management_api import db


association_table = db.Table(
    'association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'))
)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    groups = db.relationship(
        'Group',
        secondary=association_table,
        backref=db.backref('users', lazy='dynamic')
    )


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    date_created = db.Column(db.DateTime, server_default=db.func.now())
