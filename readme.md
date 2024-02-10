# Fantastic Bakery Admin Backend

## Description

The Fantastic Bakery Admin Backend is a robust backend API designed specifically for administrators to efficiently manage the inventory of a bakery. This application provides a seamless and intuitive interface for performing various inventory-related tasks, ensuring smooth operations and optimal resource utilization within the bakery.

### Key Features:

-   **Inventory Management**: Easily add, update, and remove bakery products from the inventory database.
-   **Product Categorization**: Organize bakery products into categories for better organization and navigation.
-   **Stock Tracking**: Keep track of product quantities in real-time to ensure timely replenishment and avoid stockouts.
-   **Data Insights**: Analytics to gain insights into inventory trends, sales performance, and product popularity.

## Setup

To run this project locally, follow these steps:

### 1. Clone the repository

```bash
git clone https://github.com/naazweb/fantastic-bakery-admin-backend.git
cd fantastic-bakery-admin-backend
```

### 2. Create a virtual environment (optional but recommended)

```bash
python -m venv venv
```

Activate the virtual environment:

-   On Windows

```bash
env\Scripts\activate
```

-   On macOS and Linux

```bash
source venv/bin/activate
```

### 3. Install dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The application should now be running locally. Access it at http://localhost:8000.

## Usage

### 1. API to create a Product

```cURL
curl --location 'http://127.0.0.1:8000/products/' \
--header 'Content-Type: application/json' \
--data '{
    "name": "Red Velvet Cake"
    "price": 85.32,
    "quantity":"8"
}'
```
