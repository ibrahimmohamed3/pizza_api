from flask import jsonify, request
from app import app, db
from app.models import Restaurant, Pizza, RestaurantPizza


@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address
    } for restaurant in restaurants])

# get a specific restaurant by id
@app.route('/restaurants/<int:restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        return jsonify({
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "pizzas": [{
                "id": pizza.id,
                "name": pizza.name,
                "ingredients": pizza.ingredients
            } for pizza in restaurant.pizzas]
        })
    return jsonify({"error": "Restaurant not found"}), 404

# delete a restaurant 
@app.route('/restaurants/<int:restaurant_id>', methods=['DELETE'])
def delete_restaurant(restaurant_id):
    restaurant = Restaurant.query.get(restaurant_id)
    if restaurant:
        db.session.delete(restaurant)
        db.session.commit()
        return '', 204
    return jsonify({"error": "Restaurant not found"}), 404

# get all pizzas
@app.route('/pizzas', methods=['GET'])
def get_pizzas():
    pizzas = Pizza.query.all()
    return jsonify([{
        "id": pizza.id,
        "name": pizza.name,
        "ingredients": pizza.ingredients
    } for pizza in pizzas])

# create a  RestaurantPizza
@app.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    price = data.get('price')
    pizza_id = data.get('pizza_id')
    restaurant_id = data.get('restaurant_id')
    
    # validate data and create the RestaurantPizza
    if price and 1 <= price <= 30 and pizza_id and restaurant_id:
        restaurant_pizza = RestaurantPizza(price=price, pizza_id=pizza_id, restaurant_id=restaurant_id)
        db.session.add(restaurant_pizza)
        db.session.commit()
        return jsonify({
            "id": restaurant_pizza.pizza.id,
            "name": restaurant_pizza.pizza.name,
            "ingredients": restaurant_pizza.pizza.ingredients
        }), 201
    return jsonify({"errors": ["Validation errors"]}), 400
