from flask import Flask

from .routes import bp_products

app = Flask(__name__)
app.register_blueprint(bp_products)
