"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for,g
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User,People,Planets,Fav_People,Fav_Planets
from sqlalchemy.orm import joinedload

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

@app.before_request
def before_request():
    g.my_data = {}

# Ejemplo de uso de g
@app.route("/")
def index():
    g.my_data["message"] = "Hola mundo"
    return jsonify(g.my_data)
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():
    
    all_users = User.query.all()
    new_users = []
    for i in range(len(all_users)):
        print(all_users[i].serialize())
        new_users.append(all_users[i].serialize())
    
   

    return jsonify(new_users), 200
@app.route("/user/favorites", methods=["GET"])
def get_user_favorites():
    user_email = request.args.get('email')
    print("user_email:", user_email)
    if user_email:
        fav_people = Fav_People.query.filter_by(user_fav=user_email).all()
        fav_people_list = [fav.serialize() for fav in fav_people]
        rel_planets = Fav_Planets.query.filter_by(user_fav=user_email).all()
        rel_planets_list = [fav.serialize() for fav in rel_planets]
        # en postman para que se pueda listar los favoritos de un usuario envio como url https://3000-4geeksacade-flaskresthe-6gbameuuazw.ws-us88.gitpod.io/user/favorites?email=jav20green@gmail.com con ejemplo jav20green@gmail.com
        return jsonify({'people': fav_people_list, 'planets': rel_planets_list}), 200
    else:
        return jsonify({'message': 'User email not provided'}), 400
        
@app.route("/people", methods=["GET"])
def get_all_people():

    all_people = People.query.all()
    new_people = []
    for person in all_people:
        new_people.append(person.serialize())

    return jsonify(new_people), 200

@app.route("/planets", methods=["GET"])
def get_all_planets():

    all_planets = Planets.query.all()
    new_planets = []
    for person in all_planets:
        new_planets.append(person.serialize())

    return jsonify(new_planets), 200
@app.route("/people/<int:people_id>", methods=["GET"])
def get_one_people(people_id):

     # Busca la entidad People con el id dado y carga sus datos relacionados
    person = People.query.options(joinedload(People.fav_people)).filter_by(id=people_id).first()
    return jsonify(person.serialize()), 200

@app.route("/planets/<int:planets_id>", methods=["GET"])
def get_one_planet(planets_id):

    person = Planets.query.options(joinedload(Planets.rel_planets)).filter_by(id=planets_id).first()
    return jsonify(person.serialize()), 200

@app.route("/favorite/planet/<int:planet_id>", methods=['POST'])
def post_fav_planet(planet_id):
    #en postman para que se pueda agregar otro favorito de un usuario envio como url https://3000-4geeksacade-flaskresthe-6gbameuuazw.ws-us88.gitpod.io/favorite/planet/5?email=jav20green@gmail.com

    user_email = request.args.get('email').strip()
    planet = Planets.query.get(planet_id)
    new_fav_planet = Fav_Planets(planets_name=planet.name, rel_planets=planet, user_fav=user_email)
    db.session.add(new_fav_planet)
    db.session.commit()
    
    return jsonify({
        "mensaje": "el planeta con id "+ str(planet_id) + " ha sido agregado"
    })
@app.route("/favorite/people/<int:people_id>", methods=['POST'])
def post_fav_people(people_id):
    
    #en postman para que se pueda agregar otro favorito de un usuario envio como url https://3000-4geeksacade-flaskresthe-6gbameuuazw.ws-us88.gitpod.io/favorite/planet/5?email=jav20green@gmail.com

    user_email = request.args.get('email').strip()
    people = People.query.get(people_id)
    new_fav_people = Fav_People(people_name=people.name, fav_people=people, user_fav=user_email)
    db.session.add(new_fav_people)
    db.session.commit()
    
    return jsonify({
        "mensaje": "people con id "+ str(people_id) + " ha sido agregado"
    })
@app.route("/favorite/planet/<int:planet_id>", methods=['DELETE'])
def del_fav_planet(planet_id):
    
    user_email = request.args.get('email').strip()
    rel_planets = Fav_Planets.query.filter_by(id=planet_id, user_fav=user_email).first()

    if rel_planets:
        db.session.delete(rel_planets)
        db.session.commit()
        return jsonify({
            "mensaje": "el planeta con id "+ str(planet_id) + " ha sido eliminado"
        })
    else:
        return jsonify({
            "mensaje": "No se encontró ningún personaje con el ID especificado"
        }) 
@app.route("/favorite/people/<int:people_id>", methods=['DELETE'])
def del_fav_people(people_id):
    
    user_email = request.args.get('email').strip()
    fav_people = Fav_People.query.filter_by(id=people_id, user_fav=user_email).first()

    print(fav_people)
    if fav_people:
        db.session.delete(fav_people)
        db.session.commit()
        return jsonify({
            "mensaje": "el personaje con id "+ str(people_id) + " ha sido eliminado"
        })
    else:
        return jsonify({
            "mensaje": "No se encontró ningún personaje con el ID especificado"
        })    
#para el delete nuevamente tengo que poner la url https://3000-4geeksacade-flaskresthe-6gbameuuazw.ws-us88.gitpod.io/favorite/planet/2?email=jav20green@gmail.com por ejemplo en DELETE para eliminar, pero si funciona!

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
