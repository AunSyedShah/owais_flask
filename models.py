from flask_sqlalchemy import SQLAlchemy
import json
import os
db = SQLAlchemy()

database_path = "postgresql://{}:{}@{}/{}".format(
    os.environ.get('DB_USER', 'postgres'), 
    os.environ.get('DB_PASSWORD', '12345'),
    os.environ.get('DB_HOST', 'localhost:5433'),
    os.environ.get('DB_NAME', 'casting_agency'),


)

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    with app.app_context():
        db.drop_all()


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
    !!NOTE you can change the database_filename variable to have multiple verisons of a database
'''

class Actors(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(120))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=True)


    def insert(self):
        db.session.add(self)
        db.session.commit()

        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

        
    def update(self):
        db.session.commit()
        
    def __repr__(self):
        return json.dumps(
            {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id': self.movie_id
        }
        )

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    date = db.Column(db.String(120))

    actors = db.relationship('Actors', backref="movies", lazy=True)



    def insert(self):
        db.session.add(self)
        db.session.commit()

        
    def delete(self):
        db.session.delete(self)
        db.session.commit()

        
    def update(self):
        db.session.commit()
        
    def __repr__(self):
        return json.dumps(
            {
            'id': self.id,
            'title': self.title,
            'date': self.date,
        }
        )

def db_drop_and_create_all(app):
    # with app.app_context():
        # db.drop_all()
        # db.create_all()
    # add one demo row which is helping in POSTMAN test
    try:
        with app.app_context():
            # db.drop_all()
            db.create_all()

            movie = Movies(
                title='Maula Jutt',
                date='1972-03-24'
                
            )



            movie.insert()
            actor = Actors(
                name='Mahira Khan',
                age=30,
                gender='Female',
                movie_id=movie.id

            )
            actor.insert()
    except Exception as e:
        print('errr',e)
