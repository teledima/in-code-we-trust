from flask import Flask

from .routes import bp_products, bp_sales

app = Flask(__name__)
app.register_blueprint(bp_products)
app.register_blueprint(bp_sales)
