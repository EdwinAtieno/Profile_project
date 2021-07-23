from flask import Flask, request, render_template, redirect, jsonify
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

#currentlocation = os.path.dirname(os.path.abspath(__file))
app = Flask(__name__)

db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///profile.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app.config['SECRET_KEY'] = 'MYSECRET'


class User_creation(db.Model):
    email = db.Column(db.String(50), unique=True, primary_key=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password

class UserSchema(ma.Schema):
    class Meta:
        fields = ('email','name','password')

user_schema = UserSchema(many=True)

class profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    First_name = db.Column(db.String(50))
    Last_name = db.Column(db.String(50))
    User_Name = db.Column(db.String(80), unique=True)
    City = db.Column(db.String(80))
    Country = db.Column(db.String(80))
    Portfolio = db.Column(db.String(80))
    Bio = db.Column(db.String(500))
    Skills = db.Column(db.String(80))

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password


class ProfileSchema(ma.Schema):
    class Meta:
        fields = ('First_name', 'Last_name', 'User_Name', 'City','Country','Portfolio','Bio','Skills')

profile_schema = ProfileSchema(many=True)

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User_creation(email=data['email'], name=data['name'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'new user created'})

@app.route('/user', methods=['GET'])
def get_products():
    all_user= User_creation.query.all()
    result = user_schema.dump(all_user)
    return jsonify(result)

# delete product
@app.route('/user/<email>', methods=['DELETE'])
def delete_product(email):
    product = User_creation.query.get(email)
    db.session.delete(product)
    db.session.commit()

    return user_schema.jsonify(product)

db.create_all()
app.debug=True
if __name__ == '__main__':
    app.run(debug=True)
