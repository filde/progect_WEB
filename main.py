from flask import Flask, render_template, redirect, request, make_response, jsonify
from data import db_session, projects_resource, users_resource
from data.users import User
from data.projects import Projects
from data.diplomas import Diplomas
from password_check import *
from forms.register import RegisterForm
from forms.login import LoginForm
from forms.project import ProjectsForm
from forms.user import UserForm
from forms.file import File
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from requests import get
import re
import os
from flask_restful import reqparse, abort, Api, Resource


app = Flask(__name__)
api = Api(app)
api.add_resource(projects_resource.ProjectsListResource, '/api/projects') 
api.add_resource(projects_resource.ProjectsResource, '/api/projects/<int:projects_id>')
api.add_resource(users_resource.UsersListResource, '/api/users') 
api.add_resource(users_resource.UsersResource, '/api/users/<int:users_id>')
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)
db_sess = ''


@app.errorhandler(404) # Обработка ошибки вызываемой API
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
    

def main(): # Подключение к базе данных и запуск сервера
    global db_sess
    db_session.global_init("db/blogs.db")
    db_sess = db_session.create_session()
    app.run()


@app.route("/") # Главная страница с проектами
def index():
    global db_sess
    projects = db_sess.query(Projects).filter(Projects.active)
    return render_template("projects_log.html", projects=projects, title="Проекты")


@app.route('/register', methods=['GET', 'POST']) # Регистрация пользователя
def reqister():
    global db_sess
    form = RegisterForm()
    if form.validate_on_submit():
        regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
        is_valid = re.search(regex, form.email.data)
        if not is_valid:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message='Неверный формат почты')
        st = check_new_password(form.password.data)
        if st:
           return render_template('register.html', title='Регистрация',
                                  form=form,
                                  message=st)
        if form.password.data != form.password_again.data:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пароли не совпадают")
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Такой пользователь уже есть")
        if form.age.data < 6:
            return render_template('register.html', title='Регистрация',
                                   form=form,
                                   message="Пользователь должен быть старше 5 лет")
        user = User(
            email=form.email.data,
            name=form.name.data,
            surname=form.surname.data,
            age=form.age.data,
            about=form.about.data,
            contacts=form.contacts.data
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=form)


@login_manager.user_loader
def load_user(user_id):
    global db_sess
    return db_sess.query(User).get(user_id)


@app.route('/login', methods=['GET', 'POST']) # Страница для ввода логина и пароля
def login():
    global db_sess
    form = LoginForm()
    if form.validate_on_submit():
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html', title="Авторизация",
                               message="Неправильная почта или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout') # Выход из учётной записи
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route('/new_application/<int:project_id>') # Создание новой заявки на участие в проекте
@login_required
def new_application(project_id):
    global db_sess
    project = db_sess.query(Projects).get(project_id)
    project.applications.append(current_user)
    if len(project.users) == project.count:
        project.active = False
    db_sess.commit()
    return redirect("/")


@app.route('/persona/<int:user_id>') # Профиль пользователя
def persona(user_id):
    global db_sess
    user = db_sess.query(User).get(user_id)
    return render_template('persona.html', title=user.surname + ' ' + user.name,
                           user=user)


@app.route('/edit_user', methods=['GET', 'POST']) # Изменение профиля пользователя
@login_required
def edit_user():
    global db_sess
    form = UserForm()
    if request.method == "GET":
        user = current_user
        if user:
            form.email.data = user.email
            form.surname.data = user.surname
            form.name.data = user.name
            form.age.data = user.age
            form.about.data = user.about
            form.contacts.data = user.contacts
        else:
            abort(404)
    if form.validate_on_submit():
        user = current_user
        if user:
            if db_sess.query(User).filter(User.email == form.email.data, User.id != current_user.id).first():
                return render_template('user.html', title='Редактирование профиля',
                                    form=form,
                                    message="Пользователь с такой почтой уже есть")
            if form.age.data < 6:
                return render_template('user.html', title='Редактирование профиля',
                                    form=form,
                                    message="Пользователь должен быть старше 5 лет")
            user.email = form.email.data
            user.surname = form.surname.data
            user.name = form.name.data
            user.age = form.age.data
            user.about = form.about.data
            user.contacts = form.contacts.data
            db_sess.commit()
            return redirect('/persona/' + str(current_user.id))
        else:
            abort(404)
    return render_template('user.html',
                           title='Редактирование профиля',
                           form=form)


@app.route('/projects') # Страница с проектами, в которых пользователь участвует(в том числе является лидером)
@login_required
def my_projects():
    global db_sess
    projects = current_user.project + current_user.projects
    return render_template('projects.html', title='Мои проекты', projects=projects)


@app.route('/delete/<int:id>', methods=['GET', 'POST']) # Удаление проекта
@login_required
def projects_delete(id):
    global db_sess
    projects = db_sess.query(Projects).filter(Projects.id == id, Projects.leader == current_user).first()
    if projects:
        db_sess.delete(projects)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/projects')


@app.route('/applications/<int:proj_id>') # Заявки на участие в конкретном проекте
@login_required
def applications(proj_id):
    global db_sess
    project = db_sess.query(Projects).filter(Projects.id == proj_id, Projects.leader == current_user,
                                             Projects.active).first()
    print(project)
    if project:
        people = project.applications
        return render_template('applications.html', title='Заявки на участие в проекте',
                               people=people, id=proj_id)
    else:
        abort(404)


@app.route('/application_yes/<int:user_id>/<int:project_id>') # Принятие заявки на участие в проекте его лидером
@login_required
def application_yes(user_id, project_id):
    global db_sess
    project = db_sess.query(Projects).filter(Projects.id == project_id, Projects.active).first()
    user = db_sess.query(User).get(user_id)
    if user and project and user in project.applications:
        project.applications.remove(user)
        user.projects.append(project)
        if len(project.users) == project.count:
            project.active = False
            db_sess.commit()
            return redirect('/projects')
        db_sess.commit()
        return redirect('/applications/' + str(project_id))
    else:
        abort(404)


@app.route('/application_no/<int:user_id>/<int:project_id>') # Отклонение заявки на участие в проекте его лидером
@login_required
def application_no(user_id, project_id):
    global db_sess
    project = db_sess.query(Projects).get(project_id)
    user = db_sess.query(User).get(user_id)
    if user and project and user in project.applications:
        project.applications.remove(user)
        db_sess.commit()
        return redirect('/applications/' + str(project_id))
    else:
        abort(404)


@app.route('/delete_member/<int:user_id>/<int:project_id>') # Исключение участника из проекта его лидером
@login_required
def delete_member(user_id, project_id):
    project = db_sess.query(Projects).filter(Projects.id == project_id, Projects.leader == current_user).first()
    user = db_sess.query(User).get(user_id)
    if user and project and project in user.projects:
        user.projects.remove(project)
        if len(project.users) < project.count:
            project.active = True
        db_sess.commit()
        return redirect('/projects')
    else:
        abort(404)


@app.route('/new_project',  methods=['GET', 'POST']) # Создание нового проекта
@login_required
def new_project():
    global db_sess
    form = ProjectsForm()
    if form.validate_on_submit():
        if form.count.data < 1:
            return render_template('add_project.html', title='Новый проект', form=form,
                                   message='В команде кроме лидера должен быть хотя бы ещё один участник',
                                   name='Новый проект')
        projects = Projects(
            title=form.title.data,
            count=form.count.data,
            about=form.about.data
        )
        current_user.project.append(projects)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/projects')
    return render_template('add_project.html', title='Новый проект', 
                           form=form, name='Новый проект')


@app.route('/edit_project/<int:id>', methods=['GET', 'POST']) # Редактирование проекта
@login_required
def edit_project(id):
    global db_sess
    form = ProjectsForm()
    if request.method == "GET":
        project = db_sess.query(Projects).filter(Projects.id == id, Projects.leader == current_user).first()
        if project:
            form.title.data = project.title
            form.count.data = project.count
            form.about.data = project.about
        else:
            abort(404)
    if form.validate_on_submit():
        project = db_sess.query(Projects).filter(Projects.id == id, Projects.leader == current_user).first()
        if project:
            if form.count.data < 1:
                return render_template('add_project.html', title='Редактирование проекта', form=form,
                                       message='В команде кроме лидера должен быть хотя бы ещё один участник',
                                       name='Редактирование проекта')
            if form.count.data < len(project.users):
                return render_template('add_project.html', title='Редактирование проекта', form=form,
                                       message='Не может быть количество участников меньше того, которое уже участвует в проекте',
                                       name='Редактирование проекта')
            project.title = form.title.data
            project.count = form.count.data
            project.about = form.about.data
            if len(project.users) == form.count.data:
                project.active = False
            else:
                project.active = True
            db_sess.commit()
            return redirect('/projects')
        else:
            abort(404)
    return render_template('add_project.html',
                           title='Редактирование проекта',
                           name='Редактирование проекта',
                           form=form)


@app.route('/my_applications') # Заявки пользователя на участие в других проектах
@login_required
def my_applications():
    projects = current_user.applications
    return render_template('my_applications.html', title='Отправленные заявки', projects=projects)


@app.route('/cansel/<int:project_id>') # Отменя заявки на участие в проекте
@login_required
def cansel(project_id):
    global db_sess
    project = db_sess.query(Projects).get(project_id)
    if project and current_user in project.applications:
        project.applications.remove(current_user)
        db_sess.commit()
        return redirect('/my_applications')
    else:
        abort(404)


@app.route('/out_project/<int:project_id>') # Отказ пользователя от участия в проекте
@login_required
def out_project(project_id):
    global db_sess
    project = db_sess.query(Projects).get(project_id)
    if project and current_user in project.users:
        project.users.remove(current_user)
        if len(projects.users) < project:
            projects.active = True
        db_sess.commit()
        return redirect('/projects')
    else:
        abort(404)


@app.route('/galery/<int:user_id>') # Страница с наградами пользователя
def galery(user_id):
    global db_sess
    user = db_sess.query(User).get(user_id)
    if user:
        return render_template('galery.html', sp=user.diplomas, user=user, title="Награды") 
    else:
        abort(404)



@app.route('/add_galery', methods=['GET', 'POST']) # Добавление награды
def add_galery():
    global db_sess
    form = File()
    if form.validate_on_submit():
        a = db_sess.query(Diplomas).all()
        if a:
            ind = max(a, key=lambda x: x.id).id + 1
        else:
            ind = 1
        print(ind)
        diploma = Diplomas(
            id=ind,
            title=form.title.data,
            address=str(ind) + '.jpg'
        )
        with open('static/img/' + diploma.address, 'wb') as img:
            img.write(form.image.data.read())
        current_user.diplomas.append(diploma)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/galery/' + str(current_user.id))
    return render_template('add_galery.html', title='Добавление награды', 
                           form=form, name='Добавление награды')


@app.route('/delete_galery/<int:id>') # Удаление награды
def delete_galery(id):
    global db_sess
    dip = db_sess.query(Diplomas).get(id)
    if current_user and current_user.id == dip.owner:
        os.remove('static/img/' + dip.address)
        db_sess.delete(dip)
        db_sess.commit()
        return redirect('/galery/' + str(current_user.id))
    else:
        abort(404)


if __name__ == '__main__':
    main()
