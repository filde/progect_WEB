from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify
from .projects import Projects
from . import db_session


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('team_lead', required=True, type=int)
parser.add_argument('count', required=True, type=int)
parser.add_argument('about', required=True)
parser.add_argument('active', required=True, type=bool)


def abort_if_projects_not_found(projects_id):
    session = db_session.create_session()
    projects = session.query(Projects).get(projects_id)
    if not projects:
        abort(404, message=f"Projects {projects_id} not found")


class ProjectsResource(Resource):
    def get(self, projects_id):
        abort_if_projects_not_found(projects_id)
        session = db_session.create_session()
        projects = session.query(Projects).get(projects_id)
        return jsonify({'projects': projects.to_dict(
            only=('id', 'title', 'team_lead', 'count', 'about', 
                  'created_date', 'active'))})

    def delete(self, projects_id):
        abort_if_projects_not_found(projects_id)
        session = db_session.create_session()
        projects = session.query(Projects).get(projects_id)
        session.delete(projects)
        session.commit()
        return jsonify({'success': 'OK'})
    
    def put(self, projects_id):
        args = parser.parse_args()
        session = db_session.create_session()
        projects = session.query(Projects).get(projects_id)
        if not projects:
            abort(404, message=f"Projects {projects_id} not found")
        projects.title = args['title']
        projects.team_lead = args['team_lead']
        projects.count = args['count']
        projects.about = args['about']
        projects.active = args['active']
        session.commit()
        return jsonify({'success': 'OK'})


class ProjectsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        projects = session.query(Projects).all()
        return jsonify({'projects':
                            [item.to_dict(only=('id', 'title', 'team_lead', 'count', 'about', 
                                                'created_date', 'active')) for item in projects]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        projects = Projects(
            title=args['title'],
            team_lead=args['team_lead'],
            count=args['count'],
            about=args['about'],
            active=args['active']
        )
        session.add(projects)
        session.commit()
        return jsonify({'success': 'OK'})