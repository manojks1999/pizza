# flask dependencies
from flask import Blueprint, jsonify, request, current_app
# db session
from api import db_session
from .schema import Items, Orders
from .tasks import asyncUpdate

import json
import os
import datetime

try:
    apis_blueprint = Blueprint("apis", __name__, url_prefix="/api")
    main_blueprint = Blueprint("main_apis", __name__, url_prefix="/")
except Exception as e:
    apis_blueprint = Blueprint("apis", __name__, url_prefix="/api")
    main_blueprint = Blueprint("main_apis", __name__, url_prefix="/")

def initDb():
    try:
        base_data = [
            Items( name = 'Thin Crust', price = 500, category = 'base'),
            Items( name = 'Normal', price = 400, category = 'base'),
            Items( name = 'Cheese Burst', price = 200, category = 'base')
        ]
        db_session.add_all(base_data)

        toppingss_data = [
            Items( name = 'Marinara sauce', price = 20, category = 'topping'),
            Items( name = 'Chicken breast', price = 30, category = 'topping'),
            Items( name = 'Green peppers', price = 15, category = 'topping'),
            Items( name = 'Black olives', price = 45, category = 'topping'),
            Items( name = 'Spinach', price = 20, category = 'topping'),
            Items( name = 'Mushrooms', price = 15, category = 'topping'),
            Items( name = 'Onions', price = 10, category = 'topping')
        ]
        db_session.add_all(toppingss_data)

        toppingss_data = [
            Items( name = 'Mozzarella Cheese', price = 20, category = 'cheese'),
            Items( name = 'Provolone Cheese', price = 30, category = 'cheese'),
            Items( name = 'Cheddar Cheese', price = 15, category = 'cheese'),
            Items( name = 'Gouda', price = 45, category = 'cheese')
        ]
        db_session.add_all(toppingss_data)
        db_session.commit()
    except Exception as e:
        print("ererer", e)
        raise e

# initDb()

@main_blueprint.route("/", methods=["GET"])
def api():
    try:
        # asyncUpdate.apply_async(args=({"id": "3b032898-54de-4c6b-9105-2c9fee3b52eb", "status": "delivered"},), eta=datetime.datetime.utcnow() + datetime.timedelta(seconds=10))

        return jsonify(
            {
                "success": True,
                "message": "Successfully received request"
            })
    except Exception as e:
        print("error", e)
        return jsonify({
            "success": False,
            "message": "Error while performing operation"
            }), 404


@apis_blueprint.route("/menu", methods=["GET"])
def get_menu():
    try:
        res = {
            "base": [],
            "topping": [],
            "cheese": []
        }
        data = db_session.query(Items).all()
        for ele in data:
            cat = ele.category
            res[cat].append({
                "id": ele.id,
                "name": ele.name,
                "price": ele.price
            })

        print(res)
        return jsonify(
            {
                "success": True,
                "data": res
            })
    except Exception as e:
        print("error", e)
        return jsonify({
            "success": False,
            "message": "Error while performing operation"
            }), 404
    

@apis_blueprint.route("/order", methods=["GET"])
def track_order():
    try:
        order_id = request.args["order_id"]
        data = db_session.query(Orders).filter(Orders.id == order_id).all()
        res = {}
        for ele in data:
            res["id"] = ele.id
            res["price"] = ele.total_price
            res["quantity"] = ele.quantity
            res["items"] = ele.item
            res["status"] = ele.status
            res["ordered_at"] = ele.ordered_at
            res["updated_at"] = ele.updated_at
        db_session.commit()
        return jsonify(
            {
                "success": True,
                "data": res
            })
    except Exception as e:
        print("error", e)
        return jsonify({
            "success": False,
            "message": "Error while performing operation"
            }), 404    


@apis_blueprint.route("/order", methods=["POST"])
def place_order():
    try:
        data = request.get_json()
        orders = data["data"]
        total_price = 0
        quantity = 0
        total_items = []

        for order in orders:
            base = order["base"]
            topping = order["topping"]
            cheese = order["cheese"]
            inp_ids = tuple([base, cheese] + topping)
            db_data = db_session.query(Items).filter(Items.id.in_(inp_ids)).all()
            local_item = {}
            local_price = 0

            for ele in db_data:
                if ele.category == 'base':
                    print(ele.name)
                    local_item["base"] = ele.name
                elif ele.category == 'cheese':
                    local_item["cheese"] = ele.name
                elif ele.category == 'topping':
                    # print(local_item, ele.name)
                    print([ele.name])
                    if "topping" not in local_item:
                        local_item["topping"] = [ele.name]
                    else:
                        local_item["topping"].append(ele.name)
                        
                total_price += ele.price
                local_price += ele.price
            local_item["price"] = local_price
            total_items.append(local_item)
            quantity += 1
            print(local_item)
            if "topping" not in local_item or len(local_item["topping"]) != 5 or "base" not in local_item or "cheese" not in local_item:
                return jsonify({
                    "success": False,
                    "message": "Invalid input data all fields are mandatory, base, topping(array of length 5), cheese"
                }), 400
        
        order_data = Orders(quantity=quantity, total_price=total_price, item=total_items)
        db_session.add(order_data)
        # print("order_data.id", order_data.id)
        asyncUpdate.apply_async(args=({"id": order_data.id, "status": "Accepted"},), eta=datetime.datetime.utcnow() + datetime.timedelta(seconds=10))
        asyncUpdate.apply_async(args=({"id": order_data.id, "status": "Preparing"},), eta=datetime.datetime.utcnow() + datetime.timedelta(minutes=1))
        asyncUpdate.apply_async(args=({"id": order_data.id, "status": "Dispatched"},), eta=datetime.datetime.utcnow() + datetime.timedelta(minutes=3))
        asyncUpdate.apply_async(args=({"id": order_data.id, "status": "Delivered"},), eta=datetime.datetime.utcnow() + datetime.timedelta(minutes=5))
        # order_data.status = 'Accepted'
        db_session.commit()
        return jsonify(
            {
                "success": True,
                "order_id": order_data.id
            })
    except Exception as e:
        print("ererrr", e)
        return jsonify({
            "success": False,
            "message": "Invalid input data all fields are mandatory, base, topping(array of length 5), cheese"
            }), 400


@apis_blueprint.app_errorhandler(400)
def bad_request(e):
    """
    Bad request error handler
    """
    return jsonify({"error": "bad Request."}), 400


@apis_blueprint.app_errorhandler(401)
def unauthorized_request(e):
    """
    Unauthorized request error handler
    """
    return jsonify({"error": "unauthorized access."}), 401


@apis_blueprint.app_errorhandler(403)
def forbidden_request(e):
    """
    Forbidden request error handler
    """
    return jsonify({"error": "forbidden access."}), 403


@apis_blueprint.app_errorhandler(404)
def not_found_error(e):
    """
    Resource not found error handler
    """
    return jsonify({"error": "resource not found."}), 404


@apis_blueprint.app_errorhandler(405)
def method_not_allowed_error(e):
    """
    Method not allowed error handler
    """
    return jsonify({"error": "method not allowed."}), 405


@apis_blueprint.app_errorhandler(429)
def method_not_allowed_error(e):
    """
    Method not allowed error handler
    """
    return jsonify({"error": "Too many requests check the rate limit."}), 405


@apis_blueprint.app_errorhandler(500)
def server_error(e):
    """
    Internal server error handler
    """
    return jsonify({"error": "internal server error."}), 500


@apis_blueprint.app_errorhandler(502)
def bad_gateway(e):
    """
    Bad gateway error handler
    """
    return jsonify({"error": "bad gateway error."}), 502


@apis_blueprint.app_errorhandler(503)
def service_unavailable(e):
    """
    Service unavailable error handler
    """
    return jsonify({"error": "service unavailable."}), 503


@apis_blueprint.app_errorhandler(504)
def timeout_error(e):
    """
    Timeout error handler
    """
    return jsonify({"error": "gateway timeout."}), 504