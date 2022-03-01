from APP import db, login_manager
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from datetime import datetime



class AdminTable(db.Model, UserMixin):
    '''
        AdminTable class creates 'admin_table' table in the database with the following columns:
        id, first_name, surname, username, email, and password
    '''
    id = db.Column(db.Integer(), primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    surname = db.Column(db.String(64), nullable=False)
    username = db.Column(db.String(32), nullable=False, unique=True)
    email = db.Column(db.String(1024), nullable=False, unique=True)
    password = db.Column(db.String(1024), nullable=False)

    def __init__(self, fname, sname, username, email_add, password):
        self.first_name = fname
        self.surname = sname
        self.username = username
        self.email = email_add
        self.password = password

    def check_password(self, attempted_password):
        return check_password_hash(self.password, attempted_password)


class Posts(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    post_category = db.Column(db.String(), nullable=False)
    post_content = db.Column(db.Integer(), nullable=False)
    reply_email = db.Column(db.Integer())
    date_created = db.Column(db.String(), nullable=False)

    def __init__(self, category, content, reply_email, date=datetime.now()):
        self.post_category = category
        self.post_content = content
        self.reply_email = reply_email
        self.date_created = date


@login_manager.user_loader
def load_user(user_id):
    return AdminTable.query.get(int(user_id))

# user defined function which adds and commit items to the database
def db_add_and_commit(item_to_add):
    db.session.add(item_to_add)
    db.session.commit()
