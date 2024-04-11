"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""

import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db, User, Favorite, Vehicle, Character, Planet
from admin import setup_admin
from models import db, User

# from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url.replace(
        "postgres://", "postgresql://"
    )
else:
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////tmp/test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)


# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code


# generate sitemap with all your endpoints
@app.route("/")
def sitemap():
    return generate_sitemap(app)


@app.route("/users", methods=["GET"])
def getUsers():

    users = User.query.all()

    allUsers = list(map(lambda x: x.serialize(), users))

    return jsonify(allUsers), 200


""" FAVORITES ROUTES"""


##Find Favorites from the first User Active
@app.route("/users/favorites", methods=["GET"])
def getFavorites():

    user_active = User.query.filter(User.is_active == True).first()

    favorite_list = Favorite.query.get(user_active.favorite.id)

    return jsonify(favorite_list.serialize()), 200


@app.route("/users/<int:user_id>/favorites", methods=["GET"])
def getFavoritesByUser(user_id):

    user_active = User.query.get(user_id)

    favorite_list = Favorite.query.get(user_active.favorite.id)

    return jsonify(favorite_list.serialize()), 200


##Set Favorite Planets from the first User Active
@app.route("/users/favorites/planets/<int:planet_id>", methods=["POST"])
def setFavoritePlanet(planet_id):
    # Obtener el usuario activo
    user_active = User.query.filter_by(is_active=True).first()

    if not user_active:
        return jsonify({"message": "User Not Found"}), 404

    favorite_list = user_active.favorite

    planet = Planet.query.get(planet_id)
    if planet in favorite_list.planets:
        return jsonify({"message": "The Planet is already added"}), 400

    favorite_list.planets.append(planet)

    db.session.commit()

    return jsonify({"message": "Planet Added to the Collection"}), 200


@app.route("/users/<int:user_id>/favorites/planets/<int:planet_id>", methods=["POST"])
def setFavoritePlanetByUser(user_id, planet_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User Not Found"}), 404

    favorite_list = user.favorite

    planet = Planet.query.get(planet_id)
    if planet in favorite_list.planets:
        return jsonify({"message": "The Planet is already added"}), 400

    favorite_list.planets.append(planet)

    db.session.commit()

    return jsonify({"message": "Planet Added to the Collection"}), 200


""" CHARACTER ROUTES """


@app.route("/people", methods=["GET"])
def getCharacters():

    characters = Character.query.all()
    all_Characters = list(map(lambda x: x.serialize(), characters))

    return jsonify(all_Characters), 200


@app.route("/people/<int:character_id>", methods=["GET"])
def getCharacter(character_id):

    character1 = Character.query.get(character_id)

    return jsonify(character1.serialize()), 200


@app.route("/people>", methods=["POST"])
def registeCharacter():

    request_body = request.get_json()

    earth = Character(
        name=request_body["name"],
        description=request_body["description"],
        homeworld=request_body["homeworld"],
        height=request_body["height"],
        mass=request_body["mass"],
        hair_color=request_body["hair_color"],
        skin_color=request_body["skin_color"],
        eye_color=request_body["eye_color"],
        birth_year=["birth_year"],
        gender=request_body["gender"],
        url=request_body["url"],
    )
    db.session.add(earth)
    db.session.commit()

    return jsonify(request_body), 200


@app.route("/people/<int:character_id>", methods=["PUT"])
def updateCharacter(character_id):

    request_body = request.get_json()

    character1 = Character.query.get(character_id)

    if character1 is None:
        raise APIException("Character not Found", status_code=404)

    if "name" in request_body:
        character1.name = request_body["name"]
    if "description" in request_body:
        character1.description = request_body["description"]
    if "homeworld" in request_body:
        character1.homeworld = request_body["homeworld"]
    if "height" in request_body:
        character1.height = request_body["height"]
    if "mass" in request_body:
        character1.mass = request_body["mass"]
    if "hair_color" in request_body:
        character1.hair_color = request_body["hair_color"]
    if "skin_color" in request_body:
        character1.skin_color = request_body["skin_color"]
    if "eye_color" in request_body:
        character1.eye_color = request_body["eye_color"]
    if "birth_year" in request_body:
        character1.birth_year = request_body["birth_year"]
    if "gender" in request_body:
        character1.gender = request_body["gender"]
    if "url" in request_body:
        character1.url = request_body["url"]

    db.session.commit()

    return jsonify(request_body), 200


@app.route("/people/<int:character_id>", methods=["DELETE"])
def deleteCharacter(character_id):

    character1 = Character.query.get(character_id)
    if character1 is None:
        raise APIException("Character not found", status_code=404)
    db.session.delete(character1)
    db.session.commit()

    return jsonify("ok"), 200


""" PLANET ROUTES """


@app.route("/planets", methods=["GET"])
def getPanets():

    planets = Planet.query.all()
    all_Planets = list(map(lambda x: x.serialize(), planets))

    return jsonify(all_Planets), 200


@app.route("/planets/<int:planet_id>", methods=["GET"])
def getPlanet(planet_id):

    planet1 = Planet.query.get(planet_id)

    return jsonify(planet1.serialize()), 200


@app.route("/planets", methods=["POST"])
def registePlanet():

    request_body = request.get_json()

    earth = Planet(
        name=request_body["name"],
        description=request_body["description"],
        diameter=request_body["diameter"],
        rotation_period=request_body["rotation_period"],
        orbital_period=request_body["orbital_period"],
        gravity=request_body["gravity"],
        population=request_body["population"],
        climate=request_body["climate"],
        terrain=["terrain"],
        surface_water=request_body["surface_water"],
        url=request_body["url"],
    )
    db.session.add(earth)
    db.session.commit()

    return jsonify(request_body), 200


@app.route("/planets/<int:planet_id>", methods=["PUT"])
def updatePlanet(planet_id):

    request_body = request.get_json()

    planet1 = Planet.query.get(planet_id)

    if planet1 is None:
        raise APIException("Planet not Found", status_code=404)

    if "name" in request_body:
        planet1.name = request_body["name"]
    if "description" in request_body:
        planet1.description = request_body["description"]
    if "diameter" in request_body:
        planet1.diameter = request_body["diameter"]
    if "rotation_period" in request_body:
        planet1.rotation_period = request_body["rotation_period"]
    if "orbital_period" in request_body:
        planet1.orbital_period = request_body["orbital_period"]
    if "gravity" in request_body:
        planet1.gravity = request_body["gravity"]
    if "population" in request_body:
        planet1.population = request_body["population"]
    if "climate" in request_body:
        planet1.climate = request_body["climate"]
    if "terrain" in request_body:
        planet1.terrain = request_body["terrain"]
    if "surface_water" in request_body:
        planet1.surface_water = request_body["surface_water"]
    if "url" in request_body:
        planet1.url = request_body["url"]

    db.session.commit()

    return jsonify(request_body), 200


@app.route("/planets/<int:planet_id>", methods=["DELETE"])
def deletePlanet(planet_id):

    planet1 = Planet.query.get(planet_id)
    if planet1 is None:
        raise APIException("Character not found", status_code=404)
    db.session.delete(planet1)
    db.session.commit()

    return jsonify("ok"), 200


""" VEHICLE ROUTES """


@app.route("/vehicles", methods=["GET"])
def getVehicles():

    vehicles = Vehicle.query.all()
    all_Vehicles = list(map(lambda x: x.serialize(), vehicles))

    return jsonify(all_Vehicles), 200


@app.route("/vehicles/<int:vehicle_id>", methods=["GET"])
def getVehicle(vehicle_id):

    vehicle1 = Vehicle.query.get(vehicle_id)

    return jsonify(vehicle1.serialize()), 200


@app.route("/vehicles", methods=["POST"])
def registeVehicles():

    request_body = request.get_json()

    earth = Vehicle(
        name=request_body["name"],
        description=request_body["description"],
        model=request_body["model"],
        vehicle_class=request_body["vehicle_class"],
        manufacturer=request_body["manufacturer"],
        cost_in_credits=request_body["cost_in_credits"],
        length=request_body["length"],
        crew=request_body["crew"],
        passengers=["passengers"],
        max_atmosphering_speed=request_body["max_atmosphering_speed"],
        cargo_capacity=request_body["cargo_capacity"],
        consumables=request_body["consumables"],
        url=request_body["url"],
    )
    db.session.add(earth)
    db.session.commit()

    return jsonify(request_body), 200


@app.route("/vehicles/<int:vehicle_id>", methods=["PUT"])
def updateVehicle(vehicle_id):

    request_body = request.get_json()

    vehicle1 = Vehicle.query.get(vehicle_id)

    if vehicle1 is None:
        raise APIException("Vehicles not Found", status_code=404)

    if "name" in request_body:
        vehicle1.name = request_body["name"]
    if "description" in request_body:
        vehicle1.description = request_body["description"]
    if "model" in request_body:
        vehicle1.model = request_body["model"]
    if "vehicle_class" in request_body:
        vehicle1.vehicle_class = request_body["vehicle_class"]
    if "manufacturer" in request_body:
        vehicle1.manufacturer = request_body["manufacturer"]
    if "cost_in_credits" in request_body:
        vehicle1.cost_in_credits = request_body["cost_in_credits"]
    if "length" in request_body:
        vehicle1.length = request_body["length"]
    if "crew" in request_body:
        vehicle1.crew = request_body["crew"]
    if "passengers" in request_body:
        vehicle1.passengers = request_body["passengers"]
    if "max_atmosphering_speed" in request_body:
        vehicle1.max_atmosphering_speed = request_body["max_atmosphering_speed"]
    if "cargo_capacity" in request_body:
        vehicle1.cargo_capacity = request_body["cargo_capacity"]
    if "consumables" in request_body:
        vehicle1.consumables = request_body["consumables"]
    if "url" in request_body:
        vehicle1.url = request_body["url"]

    db.session.commit()

    return jsonify(request_body), 200


@app.route("/vehicles/<int:vehicle_id>", methods=["DELETE"])
def deleteVehicle(vehicle_id):

    vehicle1 = Vehicle.query.get(vehicle_id)
    if vehicle1 is None:
        raise APIException("Character not found", status_code=404)
    db.session.delete(vehicle1)
    db.session.commit()

    return jsonify("ok"), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT, debug=False)
