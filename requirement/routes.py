import json

from sqlalchemy.sql.elements import or_

from requirement import app
from flask import render_template, redirect, url_for, request, flash
from requirement import db
from requirement.forms import RegisterForm, LoginForm, ProjectForm, RequirementForm, RequirementFormFilter
from requirement.models import User, Project, Requirement
from flask_login import login_user, logout_user, login_required, current_user

from requirement.utils import get_dict, get_tree


@app.route("/", methods=['POST', 'GET'])
@login_required
def index():
    return redirect("/project")


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(name=form.name.data,
                              username=form.username.data,
                              email=form.email.data,
                              password=form.password1.data)
        login_user(user_to_create)
        flash('نام کاربری شما ثبت و با موفقیت وارد سیستم شدید!')
        db.session.add(user_to_create)
        db.session.commit()
        return redirect(url_for('index'))

    if form.errors != {}:
        for err in form.errors.values():
            flash(f'Error : {err}', category='danger')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash("با موفقیت وارد شدید!", category="success")
            return redirect(url_for('index'))
        else:
            flash('نام کاربری و رمز عبور نادرست می باشد', category="danger")
    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash('با موفقیت خارج شدید', category='info')
    return redirect(url_for('login_page'))


@app.route("/project", methods=['GET', 'POST'])
@login_required
def project_page():
    form = ProjectForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            project = Project(name=form.name.data, description=form.description.data, owner=current_user.id)
            db.session.add(project)
            db.session.commit()
            flash('پروژه با موفقیت ثبت شد', category='success')
        return redirect('/project')
    else:
        project = Project.query.filter_by(owner=current_user.id)
        return render_template('project.html', form=form, projects=project)


@app.route('/project/remove/<int:project_id>')
@login_required
def project_remove(project_id):
    project = Project.query.get_or_404(project_id)
    try:
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('project_page'))
    except:
        return 'مشکلی در حذف بوجود آمد'


@app.route('/req/edit/<int:req>', methods=['GET', 'POST'])
@login_required
def edit_req(req):
    re = Requirement.query.filter_by(id=req).first()
    my_project = Project.query.filter_by(id=re.project, owner=current_user.id).first()
    if my_project is None:
        return 'پروژه وجود ندارد یا دسترسی غیرمجاز است'
    if request.method == 'POST':
        form = RequirementForm()
        if form.validate_on_submit():
            re.title = form.title.data
            re.level = form.level.data
            re.priority = form.priority.data
            re.req_type = form.req_type.data
            re.changes = form.changes.data
            re.review = form.review.data
            re.evaluation = form.evaluation.data
            re.evaluation_method = form.evaluation_method.data
            re.quality_factor = form.quality_factor.data
            re.description = form.description.data
            re.parent_id = form.parent.data
        db.session.commit()
        return redirect(url_for('requirement_page', project=re.project))

    else:
        form = RequirementForm(obj=re)
        requirement_list = Requirement.query.filter_by(project=re.project)
        form.parent.choices = sorted([(0, '---')] + [(i.id, i.title) for i in requirement_list.order_by('id')])
        form.parent.process_data(re.parent_id)
        return render_template('req_edit.html', form=form)


@app.route("/requirement/<int:project>", methods=['GET', 'POST', 'PUT'])
@login_required
def requirement_page(project):
    my_project = Project.query.filter_by(id=project, owner=current_user.id).first()
    if my_project is None:
        return 'پروژه وجود ندارد یا دسترسی غیرمجاز است'
    form = RequirementForm()
    requirement_list = Requirement.query.filter_by(project=project)
    form.parent.choices = sorted([(0, '---')] + [(i.id, i.title) for i in requirement_list.order_by('id')])

    filter_form = RequirementFormFilter()
    if request.method == 'POST':
        if form.validate_on_submit():
            req = Requirement(
                title=form.title.data,
                level=form.level.data,
                priority=form.priority.data,
                req_type=form.req_type.data,
                changes=form.changes.data,
                review=form.review.data,
                evaluation=form.evaluation.data,
                evaluation_method=form.evaluation_method.data,
                quality_factor=form.quality_factor.data,
                description=form.description.data,
                parent_id=form.parent.data,
                project=int(project)
            )
            db.session.add(req)
            db.session.commit()
            flash('نیازمندی با موفقیت ثبت شد', category='success')
            return redirect(url_for("requirement_page", project=project))
        elif filter_form.validate_on_submit():
            priority = filter_form.priority.data
            req_type = filter_form.req_type.data
            changes = filter_form.changes.data
            review = filter_form.review.data
            evaluation = filter_form.evaluation.data
            evaluation_method = filter_form.evaluation_method.data
            quality_factor = filter_form.quality_factor.data

            requirement = Requirement.query.filter(Requirement.priority.in_(map(int, priority)),
                                                   Requirement.req_type.in_(map(int, req_type)),
                                                   Requirement.changes.in_(map(int, changes)),
                                                   Requirement.review.in_(map(int, review)),
                                                   Requirement.evaluation.in_(map(int, evaluation)),
                                                   Requirement.evaluation_method.in_(map(int, evaluation_method)),
                                                   Requirement.quality_factor.in_(map(int, quality_factor)),
                                                   )

            if filter_form.check.data:
                requirement = Requirement.query.filter(or_(Requirement.priority.in_(map(int, priority)),
                                                           Requirement.req_type.in_(map(int, req_type)),
                                                           Requirement.changes.in_(map(int, changes)),
                                                           Requirement.review.in_(map(int, review)),
                                                           Requirement.evaluation.in_(map(int, evaluation)),
                                                           Requirement.evaluation_method.in_(
                                                               map(int, evaluation_method)),
                                                           Requirement.quality_factor.in_(map(int, quality_factor)),
                                                           ))

            return render_template('requirement.html', requirement=requirement, form=form, project=project,
                                   filter_form=filter_form, my_project=my_project)
        else:
            return redirect(url_for("requirement_page", project=project))
    else:
        return render_template('requirement_list.html', requirement=requirement_list, form=form, project=project,
                               filter_form=filter_form, my_project=my_project)


@app.route('/requirement/remove/<int:req>')
@login_required
def requirement_remove(req):
    requirement = Requirement.query.get_or_404(req)
    my_project = Project.query.filter_by(id=requirement.project, owner=current_user.id).first()
    if my_project is None:
        return 'پروژه وجود ندارد یا دسترسی غیرمجاز است'
    try:
        db.session.delete(requirement)
        db.session.commit()
        return redirect(url_for('requirement_page', project=requirement.project))
    except:
        return 'مشکلی در حذف بوجود آمد'


@app.route('/json/<int:project>', methods=['POST', 'GET'])
@login_required
def ajax(project):
    my_project = Project.query.filter_by(id=project, owner=current_user.id).first()
    if my_project is None:
        return 'پروژه وجود ندارد یا دسترسی غیرمجاز است'
    requirement = Requirement.query.filter_by(project=project).all()
    d = get_dict(requirement, True)
    data = {"data": d}
    j = json.dumps(data, ensure_ascii=False)
    return str(j)


@app.route('/export/json/<int:project>', methods=['GET'])
@login_required
def export_json_page(project):
    my_project = Project.query.filter_by(id=project, owner=current_user.id).first()
    if my_project is None:
        return 'پروژه وجود ندارد یا دسترسی غیرمجاز است'
    requirement = Requirement.query.filter_by(project=project).all()
    d = get_dict(requirement, False)
    data = {"data": d}
    j = json.dumps(data, ensure_ascii=False)
    return str(j)


@app.route('/export/json2/<int:project>', methods=['GET'])
@login_required
def export_json2_page(project):
    my_project = Project.query.filter_by(id=project, owner=current_user.id).first()
    if my_project is None:
        return 'پروژه وجود ندارد یا دسترسی غیرمجاز است'
    requirements = Requirement.query.filter_by(parent_id=0, project=project)
    requirements_dict = {}
    requirements_dict2 = []
    for req in requirements:
        requirements_dict2.append(get_tree(req, requirements_dict))

    json_object = json.dumps(requirements_dict2, indent=4, ensure_ascii=False)
    return str(json_object)


@app.route('/export/html/<int:project_id>', methods=["GET"])
@login_required
def export_html(project_id):
    my_project = Project.query.filter_by(id=project_id, owner=current_user.id).first()
    if my_project is None:
        return 'پروژه وجود ندارد یا دسترسی غیرمجاز است'
    project = Project.query.filter_by(id=project_id).first()
    requirement = Requirement.query.filter_by(project=project_id).all()
    req = get_dict(requirement, False)
    return render_template('html_export.html', req=req, project=project)
