"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Characters, Planets, Favorites, Vehicles
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)
#endpoints
@app.route('/characters', methods=['GET'])
def add_all_characters():
    try:
        # consultar todos sus registros del modelo
        query_results = Characters.query.all()
        #imprime los registros que estamos obteniendo
        print(query_results)
        #como nos devuelve una lista debemos recorrerla con map o for:, queremos que cada elemento sea un objeto
        # funcion lamba siempre va | elemento:cada vez que se posicione en ese elmento se aplica el metodo, name de la list iterada
        result = map(lambda item:item.serialize(), query_results)
        #imprimiendo el resultado despues de iterar la lista
        print(result)
        #como de vuelve un codigo de bajo nivel en una lista, se recomienda castear con list()
        result = list(map(lambda item:item.serialize(), query_results))
        #ahora el resultado esperado es una lista con diccionarios, serialize() las convierte
        print(result)
        #lo que se vera cuando se solicite la API
        response_body = {
            "msg": "ok",
            "results" : result
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
    #obtener la info de un solo personaje
@app.route('/character/<int:character_id>', methods=['GET'])
def get_a_character(character_id):
    try:
        #probando si mi endpoint funciona:
        print(character_id)
        query_character = Characters.query.filter_by(id=character_id).first()
        #imprimiendo lo que estoy consultando
        print(query_character)
        if not query_character:
            return jsonify({"message": "Character not found"}), 404
        #volviendolo a diccionario
        result = query_character.serialize()
        response_body = {
            "msg": "ok",
            "result" : result
        }
        return jsonify(response_body), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


#Listando todos los registros de  planets
@app.route('/planets', methods=['GET'])
def add_all_planets():
    try:
        # consultando a la base de datos
        query_result = Planets.query.all()
        #imprimiendo
        print(query_result)
        #obtengo una lista con dos item, cambiandolo a formato diccionario
        new_result = map( lambda item:item.serialize(), query_result) 
        print(new_result)
        #castear
        result = list(map( lambda item:item.serialize(), query_result) )
        print(result)

        body_response = {
            "msg" : "ok",
            "result" : result
        }
        return jsonify(body_response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
# mostrar la info de un planeta segun su if 
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_a_planet(planet_id):
    try:
        print(planet_id)
        query_planet = Planets.query.filter_by(id=planet_id).first()
        print(query_planet)
        result = query_planet.serialize()
        print(result)
        if not query_planet:
            return jsonify({"message": "Planet not found"}), 404
        body_response = {
            "msg" : "ok",
            "result" : result
        }
        return jsonify(body_response), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500
# listando a todos los usuarios
@app.route('/users', methods=['GET'])
def get_all_users():
    #accediendo a la base de datos
    query_users = User.query.all()
    print(query_users)
    #mapeando para recorrer cada item
    resutls = map(lambda item:item.serialize(), query_users)
    print(resutls)
    #casteamos
    new_result = list(resutls) 
    print(new_result)
    response_body = {
        "msg" : "ok",
        "result" : new_result
        
    }
    return jsonify(response_body), 200
# [GET] /users/favorites Listar todos los favoritos que pertenecen al usuario actual.
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites(user_id):
    try:
        #asi obtiene un usuario en especifico : User.query.get(1), usuario con id 1
        #listas de fav de un usuario basado en su id, user_id<>clave foranea, relaciona los fav con un usuario
        favorites = Favorites.query.filter_by(user_id=user_id).all()#primer user_id son los fav relacionador del user y 2do es el dato que se va introducir
        print(favorites)
        #Manejo de la Ausencia de Resultados:
        if not favorites:
            return jsonify({"msg" : "not found"}),404
        #Serialización de los Resultados, para convertilo a un objeto, ojo que es una lista 
        serialized_favorites = [f.serialize() for f in favorites]
        print(serialized_favorites)
        
        return jsonify({"msg" : "ok", "result" : serialized_favorites}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500



#[POST] /favorite/planet/<int:planet_id> Añade un nuevo planet favorito al usuario actual con el id = planet_id.
#agregar un planeta a los fav del usuario en un base de datos
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planet(planet_id):
    #imprimiendo lo que recibe, recibe un id
    print(planet_id)
    try:
        user = User.query.get(1)  
        #obtener al planeta por su id
        planeta = Planets.query.filter_by(id=planet_id).first()
        #validacion
        if not planeta:
            return jsonify({"message": "Planet not found"}), 404
        #creacion de una relacion de favorito , una nueva instancia
        favorite = Favorites(user_id=user.id, planet_id=planet_id)
        #guarda fav en la base de datos 
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"message": "Planet added to favorites"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_person(people_id):
    try:
        user = User.query.get(1) 
        #obtener al personaje por su id
        person = Characters.query.get(people_id)


        #validacion
        if not person:
            return jsonify({"message": "Character not found"}), 404
        
        #creacion de una relacion de favorito , una nueva instancia
        favorite = Favorites(user_id=user.id, character_id=people_id)

        #guarda en la base de datos 
        db.session.add(favorite)
        db.session.commit()
        return jsonify({"message": "Character added to favorites"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def remove_favorite_planet(planet_id):
    try:
        user = User.query.get(1)
        #creando una relacion 
        favorite = Favorites.query.filter_by(user_id=user.id, planet_id=planet_id).first()
        #validacion
        if not favorite:
            return jsonify({"message": "Favorite not found"}), 404
        #guarda en la base de datos 
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite planet removed"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def remove_favorite_person(people_id):
    try:
        user = User.query.get(1)  
        #creando una relacion 
        favorite = Favorites.query.filter_by(user_id=user.id, character_id=people_id).first()
        # validacion
        if not favorite:
            return jsonify({"message": "Favorite not found"}), 404
        #guarda en la base de datos 
        db.session.delete(favorite)
        db.session.commit()
        return jsonify({"message": "Favorite character removed"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)