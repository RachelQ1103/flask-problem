from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import sql

import time
import shutil


db_path = 'problem.db'
app = Flask(__name__)
app.secret_key = 'asdjf3413'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(db_path)


db = SQLAlchemy(app)


class Problem(db.Model):
    __tablename__ = 'problem'
    id = db.Column(db.Integer, primary_key=True)
    link = db.Column(db.String())
    timestamp = db.Column(db.DateTime(timezone=True), default=sql.func.now())
    status = db.Column(db.Boolean, default=False)

    def __init__(self, form):
        self.link = form.get('link', '')

    def __repr__(self):
        return u'<{} {} {}'.format(self.__class__.__name__,  self.id, self.link)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def table_row(self):
        tr = {
            'link': '<a href="{}">{}</a>'.format(self.link, self.link),
            'time': self.timestamp,
            'status': self.status,
        }
        return tr



def backup_db():
    backup_path = '{}.{}'.format(time.time(), db_path)
    shutil.copyfile(db_path, backup_path)


def rebuild_db():
    backup_db()
    db.drop_all()
    db.create_all()
    print('rebuild database')


if __name__ == '__main__':
    rebuild_db()



