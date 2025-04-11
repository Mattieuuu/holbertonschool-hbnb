# Import de l'application Flask
from app import create_app

# Création de l'instance de l'application avec la configuration de développement
# La configuration est chargée depuis le fichier config.py
app = create_app("config.DevelopmentConfig")

# Point d'entrée principal de l'application
if __name__ == '__main__':
    # Lancement du serveur en mode debug
    # Le mode debug permet le rechargement automatique lors des modifications
    # et affiche les erreurs détaillées
    app.run(debug=True)