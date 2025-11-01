# Python-Inventory

A web-based inventory management system built with Flask and MySQL. This application allows users to manage product inventory with features to add, edit, view, and delete products.

## Features

- **User Authentication**: Secure login system to protect inventory data
- **Add Products**: Add new products with name, price, and quantity
- **View Products**: Display all products in inventory with their details
- **Edit Products**: Update product price and quantity
- **Delete Products**: Remove products from inventory
- **Product Validation**: Prevents duplicate product entries

## Technologies Used

- **Python 3.x**: Backend programming language
- **Flask**: Web framework
- **MySQL**: Database for storing product information
- **HTML/CSS**: Frontend interface
- **mysql-connector-python**: Python MySQL database connector

## Installation

### Prerequisites

- Python 3.x installed
- MySQL Server installed and running
- pip package manager

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Jeyd0/Python-Inventory.git
   cd Python-Inventory
   ```

2. **Install required Python packages**
   ```bash
   pip install Flask
   pip install Flask-MySQL-Connector
   pip install mysql-connector-python
   ```

3. **Set up the database**
   - Import the `fds.sql` file into your MySQL database
   - You can use phpMyAdmin or MySQL command line:
   ```bash
   mysql -u root -p < fds.sql
   ```

4. **Configure database connection**
   - Open `app.py` and update the database connection settings if needed:
   ```python
   host='localhost'
   database='fds'
   user='root'
   password=''  # Update with your MySQL password
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

6. **Access the application**
   - Open your web browser and navigate to: `http://localhost:5000`

## Usage

### Default Login Credentials
- **Username**: jade
- **Password**: gwapo

### Managing Products

1. **Dashboard**: After logging in, you'll see the main dashboard with options to manage products
2. **Add Product**: Navigate to add product page and enter product name, price, and quantity
3. **View Products**: See all products in your inventory with their current details
4. **Edit Product**: Click edit on any product to update its price or quantity
5. **Delete Product**: Remove products that are no longer needed from your inventory

## Database Structure

The application uses a single `products` table with the following structure:
- `id`: Primary key (auto-increment)
- `name`: Product name (varchar)
- `price`: Product price (integer)
- `quantity`: Product quantity (integer)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.