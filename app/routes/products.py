from flask import Blueprint, jsonify, request
from sqlalchemy import delete, select

from app.database import SessionLocal
from app.models import Product

bp_products = Blueprint('bp_products', __name__, url_prefix='/api/products')


@bp_products.get('')
def get_products():
    with SessionLocal() as session:
        products = session.execute(select(Product)).scalars()
        return jsonify([
            {
                'id': product.id,
                'name': product.name,
                'category_id': product.category_id
            }
            for product in products
        ])


@bp_products.post('')
def create_product():
    # Получаем данные из запроса
    data = request.get_json()

    # Валидация входных данных
    if not data or 'name' not in data or 'category_id' not in data:
        return jsonify({'error': 'Name and category_id are required'}), 400

    try:
        with SessionLocal() as session:
            # Создаем новый продукт
            new_product = Product(
                name=data['name'],
                category_id=data['category_id']
            )

            # Добавляем и коммитим
            session.add(new_product)
            session.commit()

            # Возвращаем созданный продукт
            return jsonify({
                'id': new_product.id,
                'name': new_product.name,
                'category_id': new_product.category_id
            }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_products.put('')
def update_product():
    # Получаем данные из запроса
    data = request.get_json()

    # Валидация входных данных
    if not data or 'id' not in data or 'name' not in data or 'category_id' not in data:
        return jsonify({'error': 'Id, name and category_id are required'}), 400

    try:
        with SessionLocal() as session:
            # Создаем новый продукт
            product_for_update = session.execute(select(Product).where(Product.id == data['id'])).scalar()

            if not product_for_update:
                return jsonify({'error': 'Product not found'}), 404

            # Добавляем и коммитим
            product_for_update.name = data['name']
            product_for_update.category_id = data['category_id']
            session.commit()

            # Возвращаем обновленный продукт
            return jsonify({
                'id': product_for_update.id,
                'name': product_for_update.name,
                'category_id': product_for_update.category_id
            }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@bp_products.delete('<int:product_id>')
def delete_product(product_id: int):
    # Валидация входных данных
    with SessionLocal() as session:
        session.execute(delete(Product).where(Product.id == product_id))
        session.commit()

        return jsonify({'success': 'Product was deleted'}), 200
