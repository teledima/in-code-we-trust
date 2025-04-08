from datetime import date

from flask import Blueprint, request
from sqlalchemy import func, select

from app.cache import cache
from app.database import SessionLocal
from app.models import Product, Sales

bp_sales = Blueprint('sales', __name__, url_prefix='/api/sales')

DEFAULT_TTL = 60 * 5


def get_cache_key():
    return request.args.get('start_date') + ':' + request.args.get('end_date')


@bp_sales.before_request
def validate_dates():
    start_date, end_date = request.args.get('start_date'), request.args.get('end_date')

    if start_date is None or end_date is None:
        return 'You must specify the dates.'

    start_date = date.fromisoformat(start_date)
    end_date = date.fromisoformat(end_date)

    if start_date > end_date:
        return {'error': 'Start date cannot be greater than end date.'}, 400


@bp_sales.get('/total')
@cache.cached(ttl=DEFAULT_TTL, key_factory=get_cache_key)
def get_total():
    start_date, end_date = date.fromisoformat(request.args['start_date']), date.fromisoformat(request.args['end_date'])

    with SessionLocal() as session:
        total = session.execute(select(func.sum(Sales.amount)).where(Sales.dt.between(start_date, end_date)))
        return {'total': total.scalar()}, 200


@bp_sales.get('/top-products')
@cache.cached(ttl=DEFAULT_TTL, key_factory=get_cache_key)
def get_top_products():
    start_date, end_date = date.fromisoformat(request.args['start_date']), date.fromisoformat(request.args['end_date'])

    with SessionLocal() as session:
        top_products = session.execute(
            select(Product, func.sum(Sales.amount))
            .join(Sales)
            .where(Sales.dt.between(start_date, end_date))
            .group_by(Product.id)
            .order_by(func.sum(Sales.amount).desc())
            .limit(10)
        )

        return {
            'top_products': [
                {
                    'product': {
                        'id': top_product[0].id,
                        'name': top_product[0].name,
                        'category_id': top_product[0].category_id
                    },
                    'amount': top_product[1]
                }
                for top_product in top_products
            ]
        }, 200
