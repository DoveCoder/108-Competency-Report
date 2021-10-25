from flask import Flask, abort, render_template, request
from mock_data import mock_data
import json

app = Flask(__name__) # magic variable (name)
print(__name__)

coupon_codes = [ 
    {
        "code": "qwerty",
        "discount": 10
    }
]

me = {
    "name": "Jimmy",
    "last": "Newtron",
    "age": 50,
    "email": "AlienInvasion@N64.com",
    "hobbies": [],
    "address": {
        "street": "EverGreen",
        "city": "Springfield",
    }
}


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about") # route should always start with a /
def about():
    # return full name from dictionary
    return render_template("about.html")

@app.route("/about/email")
def email():
    return me["email"]

@app.route("/about/address")
def address():
    return me["address"]["street"] + " " + me["address"]["city"]

@app.route("/test")
def test():
    return "Hello there!"



#############################
###### API Methods
#############################


@app.route("/api/catalog")
def get_catalog():
    return json.dumps(mock_data)


@app.route("/api/catalog", methods=["POST"])
def save_product():
    # get request payload (body)
    product = request.get_json()

    # data validation 
    # 1 title exist and is longer than 5 chars
    if not 'title' in product or len(product["title"]) < 5:
        return abort(400, "Title is required, and should contains at least 5 chars") # 400 = bad request

    # if not 'price' in product or not isinstance(product['price'], float) <= 0:
    #     return about(400, "Price is required, and should be a positive number > 0") # 400 = bad request

    if not 'price' in product:
        return abort(400, "Price is required")

    if not isinstance(product["price"], float) and not isinstance(product["price"], int):
        return abort(400, "Price should a valid float number")

    if product['price'] <= 0:
        return abort(400,"Price should be greater than 0")

    ## validate that title exist in the dic, if not abort(400)

    #save the product
    mock_data.append(product)

    product["_id"] = len(product["title"])

    return json.dumps(product)

## /api/categories
#returns the list (string) of UNIQUE categories

@app.route("/api/categories")
def get_categories():
    categories = []
    for prod in mock_data:
        if prod["category"] not in categories:
            categories.append(prod["category"])
    return json.dumps(categories)
        

@app.route("/api/product/<id>")
def get_product(id):
    for prod in mock_data:
        if prod["_id"] == id:
            return prod
    return abort(404)


@app.route("/api/catalog/<category>")
def get_category(category):
    category_list = []

    for prod in mock_data:
        if prod["category"] == category:
            category_list.append(prod)
    return json.dumps(category_list)


@app.route("/api/cheapest")
def cheapest():
    result = mock_data[0]
    for prod in mock_data:

        if prod['price'] < result["price"]:
            result = prod
    return json.dumps(result)
             


##########################
####  Coupon Codes #######
##########################

# Post to /api/couponCodes
@app.route("/api/couponCodes")
def post_coupon():
    coupon = request.get_json()

    # validations

    #save
    coupon_codes.append(coupon)
    coupon["_id"] = coupon["code"]
    return json.dumps(coupon)

# Get to /api/couponCodes
@app.route("/api/couponCodes", methods=["GET"])
def get_coupon():
        return json.dumps(coupon_codes)

# start the server
# debug true will restart the server automatically
app.run(debug=True)