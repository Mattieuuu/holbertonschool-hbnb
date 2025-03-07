# 🏡 MyBnB - Modern BnB Platform

## Project Overview
A RESTful API for a Bed and Breakfast service built with C, following modular programming principles.

## Project Structure
```bash
part2/
├── app/
│   ├── api/v1/          # API endpoints
│   │   ├── users.py
│   │   ├── places.py
│   │   ├── reviews.py
│   │   └── amenities.py
│   ├── models/          # Business logic
│   │   ├── base_model.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/        # Facade pattern
│   └── persistence/     # Repository pattern
├── run.py              
└── requirements.txt    
```
## Compilation & Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Core Components

### Base Model
Defines a base structure with unique identifiers and timestamps.

### 📦 Core Models
- **User**: Contains user information such as name, email, and admin status.
- **Place**: Represents a rental property with attributes like title, description, price, and location.
- **Review**: Stores user-generated reviews with ratings and references to users and places.
- **Amenity**: Lists available amenities with names and relationships to places.

##  Facade Pattern
Encapsulates the main operations of the system, providing an interface to manage users, places, reviews, and amenities.

## API Endpoints & Examples

### User Management
- Create a user with first name, last name, and email.
- Retrieve and manage user details.

### Place Management
- Create and retrieve places with owner details, amenities, and reviews.
- Manage rental listings efficiently.

### Review Management
- Add reviews with text, ratings, and references to users and places.
- Retrieve and manage reviews for specific locations.

### Amenity Management
- Define and retrieve amenities associated with places.

## Common Response Format
Standardized JSON responses include unique identifiers, timestamps, and resource-specific attributes.

## Running the Application
```bash
python run.py  # Server starts at http://localhost:5000
```
