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
from models import db, User, Characters, Planets
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
    #obtener la info de un solo personaje
@app.route('/character/<int:character_id>', methods=['GET'])
def get_a_character(character_id):
    #probando si mi endpoint funciona:
    print(character_id)
    query_character = Characters.query.filter_by(id=character_id).first()
    #imprimiendo lo que estoy consultando
    print(query_character)
    #volviendolo a diccionario
    result = query_character.serialize()
    response_body = {
        "msg": "ok",
        "result" : result
    }
    return jsonify(response_body), 200

#Listando todos los registros de  planets
@app.route('/planets', methods=['GET'])
def add_all_planets():
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
# mostrar la info de un planeta segun su if 
@app.route('/planet/<int:planet_id>', methods=['GET'])
def get_a_planet(planet_id):
    print(planet_id)
    query_planet = Planets.query.filter_by(id=planet_id).first()
    print(query_planet)
    result = query_planet.serialize()
    print(result)
    body_response = {
        "msg" : "ok",
        "result" : result
    }
    return jsonify(body_response), 200












   


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
