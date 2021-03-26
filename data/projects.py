import sqlalchemy
import datetime
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm
   

association_table = sqlalchemy.Table(
    'users_to_projects',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('projects', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('projects.id'))
)

   
class Projects(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'projects'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, 
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    team_lead = sqlalchemy.Column(sqlalchemy.Integer, 
                                  sqlalchemy.ForeignKey('users.id'))
    count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, 
                                     default=datetime.datetime.now)
    about = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
    leader = orm.relation('User')
    applications = orm.relation('User',
                                secondary='projects_applications',
                                backref='applications')