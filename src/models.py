from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)
    favorite = db.relationship("Favorite", uselist=False, lazy=True)

    def __repr__(self):
        return "<User %r>" % self.email

    def serialize(self):

        favorite_data = None

        if self.favorite:
            favorite_data = {
                "id": self.favorite.id,
                "name": self.favorite.name,
            }

        return {
            "id": self.id,
            "email": self.email,
            "is_active": self.is_active,
            "favorite": favorite_data,
        }


class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=False, nullable=False)
    planets = db.relationship("Planet", secondary="favorite_planet")
    characters = db.relationship("Character", secondary="favorite_character")
    vehicles = db.relationship("Vehicle", secondary="favorite_vehicle")
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    user = db.relationship("User", back_populates="favorite")

    def serialize(self):

        planets_data = [planet.serialize() for planet in self.planets]
        characters_data = [character.serialize() for character in self.characters]
        vehicles_data = [vehicle.serialize() for vehicle in self.vehicles]

        return {
            "id": self.id,
            "name": self.name,
            "planets": planets_data,
            "characters": characters_data,
            "vehicles": vehicles_data,
        }


favorite_planet = db.Table(
    "favorite_planet",
    db.metadata,
    db.Column("favorite_id", db.ForeignKey("favorite.id")),
    db.Column("planet_id", db.ForeignKey("planet.id")),
)

favorite_character = db.Table(
    "favorite_character",
    db.metadata,
    db.Column("favorite_id", db.ForeignKey("favorite.id")),
    db.Column("character_id", db.ForeignKey("character.id")),
)

favorite_vehicle = db.Table(
    "favorite_vehicle",
    db.metadata,
    db.Column("favorite_id", db.ForeignKey("favorite.id")),
    db.Column("vehicle_id", db.ForeignKey("vehicle.id")),
)


class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.Text, unique=False, nullable=False)
    diameter = db.Column(db.Float, unique=False, nullable=False)
    rotation_period = db.Column(db.Float, unique=False, nullable=False)
    orbital_period = db.Column(db.Float, unique=False, nullable=False)
    gravity = db.Column(db.Float, unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    climate = db.Column(db.Float, unique=False, nullable=False)
    terrain = db.Column(db.Float, unique=False, nullable=False)
    surface_water = db.Column(db.Float, unique=False, nullable=False)
    url = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<Planet %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "name": self.name,
            "diameter": self.diameter,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "gravity": self.gravity,
            "population": self.population,
            "climate": self.climate,
            "terrain": self.terrain,
            "surface_water": self.surface_water,
            "url": self.url,
        }


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    homeworld = db.Column(db.String(120), unique=False, nullable=False)
    height = db.Column(db.Float, unique=False, nullable=False)
    mass = db.Column(db.Float, unique=False, nullable=False)
    hair_color = db.Column(db.String(120), unique=False, nullable=False)
    skin_color = db.Column(db.String(120), unique=False, nullable=False)
    eye_color = db.Column(db.String(120), unique=False, nullable=False)
    birth_year = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)
    url = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<Character %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "homeworld": self.homeworld,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "skin_color": self.skin_color,
            "eye_color": self.eye_color,
            "birth_year": self.birth_year,
            "gender": self.gender,
            "url": self.url,
        }


class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=False, nullable=False)
    description = db.Column(db.String(120), unique=False, nullable=False)
    model = db.Column(db.String(120), unique=False, nullable=False)
    vehicle_class = db.Column(db.String(120), unique=False, nullable=False)
    manufacturer = db.Column(db.String(120), unique=False, nullable=False)
    cost_in_credits = db.Column(db.Float, unique=False, nullable=False)
    length = db.Column(db.Float, unique=False, nullable=False)
    crew = db.Column(db.Float, unique=False, nullable=False)
    passengers = db.Column(db.Float, unique=False, nullable=False)
    max_atmosphering_speed = db.Column(db.Float, unique=False, nullable=False)
    cargo_capacity = db.Column(db.Float, unique=False, nullable=False)
    consumables = db.Column(db.String(120), unique=False, nullable=False)
    url = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return "<Vehicle %r>" % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "model": self.model,
            "vehicle_class": self.vehicle_class,
            "manufacturer": self.manufacturer,
            "cost_in_credits": self.cost_in_credits,
            "length": self.length,
            "crew": self.crew,
            "passengers": self.passengers,
            "max_atmosphering_speed": self.max_atmosphering_speed,
            "cargo_capacity": self.cargo_capacity,
            "consumables": self.consumables,
            "url": self.url,
        }
