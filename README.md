# Projet Big Data avec OAuth & OpenAI

Cette application Flask démontre l'intégration d'OAuth pour l'authentification Google et utilise l'API d'OpenAI pour générer du contenu créatif personnalisé basé sur les données de l'utilisateur.

## Fonctionnalités

- **Intégration OAuth** : Permet aux utilisateurs de s'authentifier en utilisant leur compte Google.
- **Accès au Profil Utilisateur** : Récupère et affiche les informations de base du profil utilisateur.
- **Génération de Contenu Dynamique** : Utilise le modèle GPT d'OpenAI pour créer des paroles de chansons personnalisées.

## Prérequis

Avant de démarrer, assurez-vous d'avoir Python et pip installés sur votre machine. Vous aurez également besoin de créer et d'activer un environnement virtuel pour gérer les dépendances.

## Configuration des APIs Google et OpenAI

Pour que cette application fonctionne correctement, vous devez configurer des applications sur Google Cloud Console et OpenAI pour obtenir vos clés d'API.

### Configuration de l'API Google

1. **Créer un projet sur Google Cloud Console** :
   - Rendez-vous sur [Google Cloud Console](https://console.cloud.google.com/).
   - Cliquez sur `Créer un projet`, donnez-lui un nom et suivez les instructions pour le créer.

2. **Activer l'API OAuth** :
   - Dans le tableau de bord du projet, naviguez vers `APIs & Services > Bibliothèque`.
   - Recherchez `Google+ API` et `Google People API`, puis activez-les pour votre projet.

3. **Configurer les identifiants OAuth** :
   - Allez dans `APIs & Services > Identifiants`.
   - Cliquez sur `Créer des identifiants` puis sélectionnez `ID client OAuth`.
   - Configurez l'écran de consentement, puis ajoutez les URI de redirection requis par votre application Flask.
   - Une fois les identifiants créés, notez le `client_id` et le `client_secret`.

### Configuration de l'API OpenAI

1. **Créer un compte sur OpenAI** :
   - Allez sur le site web d'[OpenAI](https://www.openai.com/) et inscrivez-vous pour un compte.

2. **Obtenir les clés API** :
   - Une fois connecté, naviguez vers l'onglet `API` sur votre tableau de bord.
   - Générez une nouvelle clé API et notez-la pour l'utiliser dans votre application.

### Intégration des clés dans votre projet

Après avoir obtenu vos clés API pour Google et OpenAI, vous devrez les intégrer manuellement dans le code source de l'application pour activer les fonctionnalités d'authentification et d'accès à l'API.

1. **Ouvrir le fichier `app.py`** :
   Localisez le fichier `app.py` dans votre projet.

2. **Ajouter les clés API Google** :
   Trouvez les lignes où `client_id` et `client_secret` sont définis pour l'objet `oauth.register` sous le nom `'google'`. Remplacez les valeurs vides par vos clés respectives obtenues :
   ```python
   oauth.register(
       name='google',
       client_id='votre_client_id',
       client_secret='votre_client_secret',
       ...
   )
 et pour Open AI
 ```
client = OpenAI(
    api_key='votre_clé_api'
)

 ```

## Configuration de l'Environnement

1. **Création de l'environnement virtuel** :
   Pour créer un nouvel environnement virtuel, ouvrez un terminal et exécutez :

```
python -m venv .venv
```


2. **Activation de l'environnement virtuel** :
- Sur Windows, activez l'environnement en exécutant :
  ```
  .\venv\Scripts\activate
  ```
- Sur macOS et Linux :
  ```
  source venv/bin/activate
  ```

3. **Installation des dépendances** :
Une fois l'environnement activé, installez toutes les dépendances nécessaires en exécutant :

```
pip install -r requirements.txt
```
## Démarrage

Pour lancer l'application, exécutez :
```
flask run
```
Cela démarrera le serveur de développement local et l'application sera accessible via `localhost:5000` par défaut.

## Utilisation

Naviguez vers `localhost:5000` dans votre navigateur. Utilisez le bouton de connexion pour vous authentifier avec Google, puis explorez les fonctionnalités de génération de contenu personnalisé.

## Sécurité

N'oubliez pas de sécuriser vos clés d'API et de ne pas les exposer publiquement. Utilisez des variables d'environnement ou d'autres méthodes sécurisées pour gérer les informations sensibles.

