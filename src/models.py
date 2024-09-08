from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#instancia para interactuar con la db.Model de datos
db = SQLAlchemy()

#Users, clase que hereda de db.Model, modelo Alchemy, se mapeara en una db.Model de datos
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(250), nullable=False)
    first_name = db.Column(db.String(250), nullable=False)
    last_name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    fecha_suscrip = Column(DateTime, nullable=False, default=datetime.utcnow)

    # favorites = db.relationship('Favorites', backref='user', lazy=True)
    # Relación uno a muchos con Favorite
    favorites = db.relationship('Favorites', back_populates='user')

    def __repr__(self):
        # aqui va la propiedad de id ya que es primary_key
        return '<User %r>' % self.id
    # convertir el objeto user en un diccionario
    def serialize(self):
         return {
            # propiedades que va ver el usuario
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "first name": self.first_name,
            "last name": self.last_name,
            # no deberías incluir la contraseña en la serialización
            # para evitar exponerla en respuestas JSON
        }
    
class Characters(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    hair_color = db.Column(db.String(250))
    eyes_color = db.Column(db.String(250))
    gender = db.Column(db.String(250))
    # planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    # favorites = db.relationship('Favorites', backref='characters', lazy=True)
    # vehicle = db.relationship('Vehicles', backref='characters', lazy=True)
    def __repr__(self):
        return '<Characters %r>' % self.id
    # convertir el objeto user en un diccionario
    def serialize(self):
         return {
            # propiedades que va ver el usuario
            "id": self.id,
            "name": self.name,
            "hair color": self.hair_color,
            "eyes color": self.eyes_color,
            "gender": self.gender,
        }

class Planets(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    population = db.Column(db.String(250))
    terrain = db.Column(db.String(250))
    # favorites = db.relationship('Favorites', backref='planets', lazy=True)
    # character = db.relationship('Characters', backref='planets', lazy=True)
    # vehicle = db.relationship('Vehicles', backref='planets', lazy=True)
   
    def __repr__(self):
        return '<Planets %r>' % self.id
    # convertir el objeto user en un diccionario
    def serialize(self):
         return {
            # propiedades que va ver el usuario
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "terrain": self.terrain,
        }

class Vehicles(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250))
    # planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=False)
    # character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=False)
    # favorites = db.relationship('Favorites', backref='vehicles', lazy=True)

    def __repr__(self):
        return '<Vehicles %r>' % self.id
    # convertir el objeto user en un diccionario
    def serialize(self):
         return {
            # propiedades que va ver el usuario
            "id": self.id,
            "name": self.name,
        }

    # def to_dict(self):
    #     return {}
    
class Favorites(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True)
    
    #Relaciones y Relaciones Inversas (Backref), si deseas acceder a los favoritos desde user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #indicando que desde user puedo acceder a favorites, con backref

    user = db.relationship('User', back_populates='favorites')



    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))
    character = db.relationship('Characters')


    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship('Planets')

# nullable=False, asegura que el valor este siempre presente
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.id'))
    vehicle = db.relationship('Vehicles')

    def __repr__(self):
        return '<Favorites %r>' % self.id
    # convertir el objeto user en un diccionario
    def serialize(self):
         return {
            # propiedades que va ver el usuario
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
            "planet_id": self.planet_id,
            "vehicle_id": self.vehicle_id

        }


























































# class User(db.Model):
#     id = db.db.Column(db.db.Integer, primary_key=True)
#     email = db.db.Column(db.db.String(120), unique=True, nullable=False)
#     password = db.db.Column(db.db.String(80), unique=False, nullable=False)
#     is_active = db.db.Column(db.Boolean(), unique=False, nullable=False)

#     def __repr__(self):
#         return '<User %r>' % self.username

#     def serialize(self):
#         return {
#             "id": self.id,
#             "email": self.email,
#             # do not serialize the password, its a security breach
#         }