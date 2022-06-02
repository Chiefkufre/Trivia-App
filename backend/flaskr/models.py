from flask_sqlalchemy import SQLAlchemy
import json



db = SQLAlchemy()

"""
setup_db(app), 
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app):
    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    db.create_all()

"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String, nullable=False)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }