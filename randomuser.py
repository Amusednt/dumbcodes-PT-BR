import random
from flask import Flask, jsonify

app = Flask(__name__)

# Predefined lists for generating random data
FIRST_NAMES = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Heidi"]
LAST_NAMES = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis"]
CITIES = ["New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "Philadelphia", "San Antonio"]
COUNTRIES = ["USA", "Canada", "Mexico", "Brazil", "UK", "Germany", "France", "Japan"]

def generate_random_user():
    """Generates a dictionary with random user data."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    email = f"{first_name.lower()}.{last_name.lower()}@{random.choice(['example.com', 'test.org', 'mail.net'])}"
    
    age = random.randint(18, 70)
    
    city = random.choice(CITIES)
    country = random.choice(COUNTRIES)
    
    # Simple "random" ID (not globally unique, just for this example)
    user_id = f"user_{random.randint(1000, 9999)}"

    return {
        "id": user_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "age": age,
        "address": {
            "city": city,
            "country": country
        }
    }

@app.route('/api/user/random', methods=['GET'])
def get_random_user():
    """API endpoint to get a single random user."""
    user_data = generate_random_user()
    return jsonify(user_data)

@app.route('/api/users/random/<int:count>', methods=['GET'])
def get_multiple_random_users(count):
    """API endpoint to get multiple random users."""
    if count <= 0:
        return jsonify({"error": "Count must be a positive integer"}), 400
    
    users = [generate_random_user() for _ in range(min(count, 100))] # Limit to 100 to prevent abuse
    return jsonify(users)

if __name__ == '__main__':
    app.run(debug=True)