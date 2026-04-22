your working directory: output_dir, do everything inside this.
create a folder named orinexa_ecommerce inside output_dir, 
inside this folder do the app development.

Build a Streamlit web application for a simple e-commerce system using JSON files for data storage (no database).

1. Tech Stack:
- Frontend & Backend: Streamlit (Python)
- Data Storage: JSON files stored inside a "database/" folder
- Use Streamlit session_state for session management

2. Project Structure:
- app.py (main app)
- database/
    - users.json
    - products.json
    - orders.json
- utils/
    - auth.py
    - product.py
    - order.py
    - storage.py (for reading/writing JSON)

3. User Roles:
- Customer
- Seller

4. Authentication:
- Register with:
  - username
  - password (store hashed)
  - role (customer/seller)
- Login system
- Store logged-in user in session_state

5. Seller Features:
- Seller dashboard
- Add product:
  - id (auto-generated)
  - name
  - price
  - stock
  - seller_id
- View their own products

6. Customer Features:
- View all products
- Search products by name
- Add to cart (store in session_state)
- Cart:
  - show items
  - show total price
- Buy products:
  - reduce stock
  - create order entry

7. Order System:
- Store orders in orders.json:
  - order_id
  - customer_id
  - items (list of products with quantity)
  - total_price
  - timestamp
- Show order history for customer

8. JSON Data Format:

users.json:
[
  {
    "id": "uuid",
    "username": "user1",
    "password": "hashed_password",
    "role": "customer"
  }
]

products.json:
[
  {
    "id": "uuid",
    "name": "shoe",
    "price": 100,
    "stock": 10,
    "seller_id": "uuid"
  }
]

orders.json:
[
  {
    "order_id": "uuid",
    "customer_id": "uuid",
    "items": [
      {"product_id": "uuid", "quantity": 2}
    ],
    "total_price": 200,
    "timestamp": "ISO datetime"
  }
]

9. Constraints:
- Prevent buying more than available stock
- Validate inputs (no negative price/stock)
- Handle empty cart
- Handle missing JSON files (initialize if not exists)

10. UI:
- Sidebar navigation:
  - Login
  - Register
  - Dashboard
- Role-based dashboard rendering

11. Bonus:
- Logout button
- Clear cart after order
- Error/success messages

Generate complete working code with modular functions.
