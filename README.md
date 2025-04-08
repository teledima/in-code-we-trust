# In Code We Trust

A Flask application with SQLAlchemy and PostgreSQL.

## Setup

1. Install Poetry if you haven't already:
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Create environment:
```bash
python3.12 -m venv venv && source venv/bin/activate
```

3. Create a PostgreSQL database named `in_code_we_trust`

4. Install dependencies:
```bash
poetry install
```

5. Initialize the database:
```bash
alembic upgrade head
```

## Running the Application

To run the application:
```bash
python run.py
```

The application will be available at `http://localhost:8000`

## API Endpoints

### Products
#### Get All Products
- **Endpoint**: `GET /api/products`
- **Description**: Retrieve a list of all products
- **Response**:
  - Status: 200 OK
  - Body: Array of product objects
    ```json
    [
      {
        "id": 1,
        "name": "Product 1",
        "category_id": 1
      },
      ...
    ]
    ```

#### Create a Product
- **Endpoint**: `POST /api/products`
- **Description**: Create a new product
- **Request Body**:
  ```json
  {
    "name": "New Product",
    "category_id": 1
  }
  ```
- **Response**:
  - Status: 201 OK
  - Body: New product object
    ```json
    {
      "id": 1,
      "name": "New Product",
      "category_id": 1
    }
    ```

#### Update a Product
- **Endpoint**: `PUT /api/products`
- **Description**: Update an existing product
- **Request Body**:
  ```json
  {
    "id": 1,
    "name": "Updated Product",
    "category_id": 1
  }
  ```
- **Response**:
  - Status: 201 OK
  - Body: Updated product object
    ```json
    {
      "id": 1,
      "name": "Updated Product",
      "category_id": 1
    }
    ```

#### Delete a Product
- **Endpoint**: `DELETE /api/products/{product_id}`
- **Description**: DELETE a product by id
- **Parameters**:
  * product_id (integer, required): ID of the product to delete


### Sales
### Get Total Sales
- **Endpoint**: `GET /api/sales/total`
- **Description**: Get total sales amount for a given date range
- **Query Parameters**:
  - `start_date` (string, required): Start date in ISO format (YYYY-MM-DD)
  - `end_date` (string, required): End date in ISO format (YYYY-MM-DD)
- **Response**:
  - Status: 200 OK
  - Body:
    ```json
    {
      "total": 12345.67
    }
    ```


### Get Top Products
- **Endpoint**: `GET /api/sales/top-products`
- **Description**: Get top 10 products by sales amount for a given date range
- **Query Parameters**:
  - `start_date` (string, required): Start date in ISO format (YYYY-MM-DD)
  - `end_date` (string, required): End date in ISO format (YYYY-MM-DD)
- **Response**:
  - Status: 200 OK
  - Body:
    ```json
    {
      "top_products": [
        {
          "product": {
            "id": 1,
            "name": "Product A",
            "category_id": 3
          },
          "amount": 5000.00
        },
        ...
      ]
    }
    ```
