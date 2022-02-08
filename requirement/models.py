from requirement import db, bcrypt, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=False)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False, unique=True)
    email = db.Column(db.String(length=50), nullable=False, unique=True)
    projects = db.relationship('Project', backref='owned_user', lazy=True)

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)


class Project(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=100), nullable=False)
    description = db.Column(db.String(length=1024))
    owner = db.Column(db.Integer, db.ForeignKey('user.id'))
    project = db.relationship('Requirement', backref='requirement_owner', cascade="all,delete", lazy=True)


class Requirement(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=400), nullable=False)
    level = db.Column(db.Integer())
    priority = db.Column(db.Integer())
    req_type = db.Column(db.Integer())
    changes = db.Column(db.Integer())
    review = db.Column(db.Integer())
    evaluation = db.Column(db.Integer())
    evaluation_method = db.Column(db.Integer())
    quality_factor = db.Column(db.Integer())
    description = db.Column(db.String(length=1024))
    project = db.Column(db.Integer(), db.ForeignKey('project.id'))

    parent_id = db.Column(db.Integer, db.ForeignKey('requirement.id'))

    parent = db.relationship('Requirement', remote_side='Requirement.id', back_populates='children', lazy=True)
    children = db.relationship('Requirement', back_populates='parent', lazy=True)
