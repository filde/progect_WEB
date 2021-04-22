from flask_restful import reqparse, abort, Api, Resource # API для пользователей
from flask import jsonify
from .users import User
from . import db_session


parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('about', required=True)
parser.add_argument('email', required=True)
parser.add_argument('password', required=True)


def abort_if_users_not_found(users_id):
    session = db_session.create_session()
    user = session.query(User).get(users_id)
    if not user:
        abort(404, message=f"User {users_id} not found")


class UsersResource(Resource): # Действия для одного пользователя
    def get(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        user = session.query(User).get(users_id)
        return jsonify({'users': user.to_dict(
            only=('id', 'surname', 'name', 'age', 'about', 'email', 'hashed_password',
                  'created_date'))})

    def delete(self, users_id):
        abort_if_users_not_found(users_id)
        session = db_session.create_session()
        user = session.query(User).get(users_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})
    
    def put(self, users_id):
        args = parser.parse_args()
        session = db_session.create_session()
        user = session.query(User).get(users_id)
        if not user:
            abort(404, message=f"User {users_id} not found")
        user.surname = args['surname']
        user.name = args['name']
        user.age = args['age']
        user.about = args['about']
        user.email = args['email']
        user.set_password(args['password'])
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource): # Действия для группы пользователей
    def get(self):
        session = db_session.create_session()
        user = session.query(User).all()
        return jsonify({'users':
                            [item.to_dict(only=('id', 'surname', 'name', 'age', 'about', 
                                                'email', 'hashed_password',
                                                'created_date')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            about=args['about'],
            email=args['email']
        )
        user.set_password(args['password'])
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})