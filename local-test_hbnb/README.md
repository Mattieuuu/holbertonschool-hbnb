### Résumé des Tâches

#### Tâche 1 : Implémentation du modèle User et de la couche logique

Dans cette tâche, tu dois créer et gérer le modèle `User` (utilisateur) dans l'application HBnB. Cela inclut la définition des attributs de l'utilisateur (prénom, nom, email, etc.) et la mise en place de la logique pour gérer les utilisateurs, y compris la création, la recherche et la gestion des données.

- **Modèle User** : Définir un modèle `User` dans un fichier Python (par exemple, `models/user.py`).
- **Création de la couche logique** : Créer un `Facade` qui agit comme un intermédiaire entre les couches de l'API et de la logique métier. Ce `Facade` contient des méthodes pour gérer les utilisateurs comme la création et la récupération.
- **API pour User** : Implémenter les points de terminaison de l'API pour créer (POST), récupérer un utilisateur (GET par ID) et la gestion d'une liste d'utilisateurs (GET pour récupérer tous les utilisateurs).

#### Tâche 2 : Implémentation des points de terminaison pour les utilisateurs

Dans cette tâche, tu dois définir les points de terminaison RESTful pour gérer les utilisateurs via l'API.

- **POST** `/api/v1/users/` : Permet de créer un utilisateur, après une validation pour vérifier que l'email n'est pas déjà pris.
- **GET** `/api/v1/users/<user_id>` : Permet de récupérer un utilisateur par son ID.
- **GET** `/api/v1/users/` : Récupère la liste des utilisateurs.
- **PUT** `/api/v1/users/<user_id>` : Permet de mettre à jour un utilisateur avec les données envoyées dans la requête.

#### Tâche 3 : Implémentation des points de terminaison pour les équipements (amenities)

Dans cette tâche, tu dois créer des points de terminaison pour gérer les équipements. Cela inclut des opérations CRUD (Créer, Lire, Mettre à jour) pour les équipements dans l'application.

- **POST** `/api/v1/amenities/` : Permet de créer un nouvel équipement.
- **GET** `/api/v1/amenities/` : Permet de récupérer tous les équipements disponibles.
- **GET** `/api/v1/amenities/<amenity_id>` : Permet de récupérer les détails d'un équipement spécifique.
- **PUT** `/api/v1/amenities/<amenity_id>` : Permet de mettre à jour les informations d'un équipement.

### Explication détaillée de la tâche 3 (Gestion des équipements)

Dans cette tâche, tu vas implémenter les points de terminaison pour gérer les équipements (amenities). L'objectif est de permettre aux utilisateurs d'ajouter, de consulter et de mettre à jour les équipements associés aux annonces dans l'application.

Voici les étapes que tu dois suivre pour cette tâche :

#### 1. Mise à jour de la couche logique (Business Logic) :

Dans le fichier `services/facade.py`, tu dois ajouter les méthodes qui permettent de manipuler les équipements. Ces méthodes incluent la création, la récupération et la mise à jour des équipements. Ces méthodes interagiront avec les repositories pour stocker et récupérer les données.

Dans `services/facade.py`, voici ce que tu dois faire :

```python
# services/facade.py

class HBnBFacade:
    def __init__(self):
        self.amenity_repo = InMemoryRepository()  # Stockage en mémoire pour les équipements

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)  # Création d'un objet Amenity à partir des données
        self.amenity_repo.add(amenity)  # Ajouter l'équipement au repository
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)  # Récupérer un équipement par ID

    def get_all_amenities(self):
        return self.amenity_repo.get_all()  # Récupérer tous les équipements

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if amenity:
            amenity.update(amenity_data)  # Mettre à jour l'équipement avec les nouvelles données
            self.amenity_repo.update(amenity)  # Sauvegarder l'équipement mis à jour
        return amenity
```

**Explications du code** :
- `create_amenity`: Crée un nouvel équipement à partir des données reçues.
- `get_amenity`: Recherche un équipement par son identifiant.
- `get_all_amenities`: Retourne la liste de tous les équipements.
- `update_amenity`: Met à jour un équipement existant.

#### 2. Mise en place des points de terminaison dans l'API (Présentation) :

Ensuite, tu dois définir les points de terminaison dans le fichier `api/v1/amenities.py` pour gérer les requêtes HTTP associées aux équipements. Cela inclut les actions pour créer, lire et mettre à jour les équipements.

Voici comment tu peux structurer ce fichier :

```python
# api/v1/amenities.py

from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('amenities', description='Operations related to amenities')

# Modèle de validation d'entrée pour les équipements
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')  # Attribut "name" requis
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity"""
        amenity_data = api.payload  # Récupérer les données envoyées dans la requête

        new_amenity = facade.create_amenity(amenity_data)  # Créer l'équipement via la couche logique
        return {'id': new_amenity.id, 'name': new_amenity.name}, 201  # Retourner l'équipement créé

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve all amenities"""
        amenities = facade.get_all_amenities()  # Récupérer tous les équipements
        return [{'id': amenity.id, 'name': amenity.name} for amenity in amenities], 200  # Retourner la liste des équipements

@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)  # Récupérer un équipement par ID
        if not amenity:
            return {'error': 'Amenity not found'}, 404  # Si l'équipement n'existe pas
        return {'id': amenity.id, 'name': amenity.name}, 200  # Retourner les détails de l'équipement

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information"""
        amenity_data = api.payload  # Récupérer les nouvelles données
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)  # Mettre à jour l'équipement
        if not updated_amenity:
            return {'error': 'Amenity not found'}, 404  # Si l'équipement n'existe pas
        return {'id': updated_amenity.id, 'name': updated_amenity.name}, 200  # Retourner l'équipement mis à jour
```

**Explications du code** :
- `AmenityList` : Ce point de terminaison permet de créer un équipement (POST) ou de récupérer la liste des équipements (GET).
- `AmenityResource` : Ce point de terminaison permet de récupérer un équipement spécifique (GET par ID) ou de mettre à jour un équipement (PUT par ID).
- `amenity_model` : Définit la structure des données attendues (un nom pour l'équipement).

#### 3. Enregistrement de l'API dans l'application Flask

N'oublie pas d'enregistrer ce namespace dans le fichier `app/__init__.py` afin que les routes soient prises en compte :

```python
# app/__init__.py

from flask import Flask
from flask_restx import Api
from app.api.v1.amenities import api as amenities_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    # Enregistrer le namespace des équipements
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    return app
```

### Récapitulatif par étapes

1. **Création de la couche logique (Facade)** :
   - Créer les méthodes `create_amenity`, `get_amenity`, `get_all_amenities`, et `update_amenity` dans le fichier `services/facade.py` pour gérer les équipements.

2. **Mise en

 place des points de terminaison API** :
   - Définir les routes dans `api/v1/amenities.py` pour gérer la création, la lecture et la mise à jour des équipements.

3. **Enregistrement de l'API dans `app/__init__.py`** :
   - S'assurer que le namespace des équipements est enregistré correctement.

4. **Tester les points de terminaison** :
   - Utiliser Postman ou cURL pour tester chaque point de terminaison (POST, GET, PUT) pour assurer le bon fonctionnement.

Cela devrait te permettre de gérer les équipements de manière fluide dans l'application HBnB !