import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin


association_table_2 = sqlalchemy.Table(
    'projects_applications',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('projects', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('projects.id'))
)


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, 
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    surname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, 
                              index=True, unique=True, nullable=True)
    age = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    project = orm.relation("Projects", back_populates='leader')
    projects = orm.relation('Projects',
                            secondary='users_to_projects',
                            backref='users')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)