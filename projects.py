import sqlalchemy
import datetime
from .db_session import SqlAlchemyBase
   

association_table = sqlalchemy.Table(
    'users_to_projects',
    SqlAlchemyBase.metadata,
    sqlalchemy.Column('users', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('users.id')),
    sqlalchemy.Column('projects', sqlalchemy.Integer,
                      sqlalchemy.ForeignKey('projects.id'))
)

   
class Projects(SqlAlchemyBase):
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
    user = orm.relation('User')
    active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)
