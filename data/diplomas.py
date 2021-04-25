import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from .db_session import SqlAlchemyBase
from sqlalchemy import orm

   
class Diplomas(SqlAlchemyBase, SerializerMixin): # Таблица с адресами картинок
    __tablename__ = 'diplomas'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, 
                           autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    owner = sqlalchemy.Column(sqlalchemy.Integer, 
                              sqlalchemy.ForeignKey('users.id'))
    address = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    user = orm.relation('User')