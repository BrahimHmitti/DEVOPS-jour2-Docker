# Apprentissages

## Problèmes rencontrés

On a vu dans Lbonnes pratiques du cours le fait d'utiliser les latest version qu'on dev mais de le figées quand on passe en prod et ce que j'ai fait dans ce tp
## Nouveau savoir

- Mécanisme des modules Go (`go.mod`, `go.sum`) : gestion reproductible des dépendances et isolation des projets.

- Structure d’une application Go HTTP (package main , negroni) : méthode reconnu pour créer rapidement des micro-services.


- **Authentification Docker Hub sous WSL** : Les helpers de credentials Windows ne fonctionnent pas correctement sous WSL, causant des erreurs d'authentification lors de l'accès au registre Docker Hub.
  - *Pourquoi* : WSL utilise un système de fichiers Linux alors que le helper de credentials est configuré pour Windows, créant un conflit lors du stockage des tokens.

- **Accès au port 3000 déjà utilisé** : Au démarrage de l'application Go, le port 3000 était parfois déjà occupé par une instance précédente.




## Solutions apportées

- **Utilisation de Personal Access Token (PAT)** : Authentification Docker Hub via PAT en désactivant le helper de credentials.


- **Configuration du port via variable d'environnement** : Modification de main.go pour récupérer le port via REDIS_HOST ou utiliser "localhost" par défaut.

au final toutes ses solutions non pas marché,j'ai utilisé powershell et ça marchait

- **Détection automatique du chemin des fichiers statiques** : Utilisation de `os.Stat("/public")` pour détecter si on est dans un conteneur.
  - *Pourquoi* : Permet d'utiliser le même code pour le développement local et le déploiement en conteneur.

## Nouveau savoir

- **Mécanisme des modules Go** (`go.mod`, `go.sum`) : gestion reproductible des dépendances et isolation des projets.
  - *Pourquoi utile* : Assure que tous les développeurs et environnements utilisent exactement les mêmes versions de dépendances.

- **Structure d'une application Go HTTP** (package main, negroni) : méthode reconnue pour créer rapidement des micro-services.
  - *Pourquoi utile* : Architecture standardisée facilitant la maintenance et l'évolution du code.

- **Multi-stage builds Docker** : Construction en deux étapes (build puis runtime) pour des images légères.
  - *Pourquoi utile* : Réduit considérablement la taille des images (< 10MB) et améliore la sécurité en n'incluant que le nécessaire.

- **Volumes Docker pour la persistance** : Configuration des volumes pour Redis afin de conserver les données.
  - *Pourquoi utile* : Permet de garder l'état de l'application même après redémarrage des conteneurs.

Partie 4 : 
- **Hot-reloading en développement** : 
  - **Go** : Utilisation d'Air pour recompiler et redémarrer automatiquement l'application lors des modifications.
  - **Python Flask** : Mode debug Flask avec `FLASK_DEBUG=1` et volumes Docker pour recharger automatiquement le code.
  - *Pourquoi utile* : Accélère le cycle de développement en évitant les étapes manuelles de compilation/redémarrage.

- **Stack Python Flask avec hot-reload** :
  - Configuration des variables d'environnement Flask (`FLASK_ENV=development`, `FLASK_DEBUG=1`)
  - Montage de volumes Docker pour synchroniser le code en temps réel
  - Gestion des dépendances Python avec `requirements.txt`
  - *Pourquoi utile* : Permet un développement rapide avec rechargement automatique sans reconstruire l'image

*TESTS* on a ajouté des nouvelles valeurs dans la guestbook ensuite on a down les containers et qu'on a rebuild on a trouvé toujours les valeurs.

*TESTS HOT-RELOAD FLASK* : Modification du titre dans `app.py` et rechargement automatique observé dans le navigateur sans redémarrage manuel.




# Flask Hot Reload Stack

## Structure

```
python-flask/
├── app.py                    # Application Flask principale
├── requirements.txt          # Dépendances Python
├── Dockerfile.dev           # Image Docker pour développement
├── docker-compose.dev.yaml  # Configuration des services
└── README.md               # Cette documentation
```

## Utilisation

### Démarrer la stack

```bash
cd stacks/python-flask
docker-compose -f docker-compose.dev.yaml up --build
```

### Accéder à l'application

- **Interface web** : http://localhost:3002
- **API messages** : 
  - GET http://localhost:3002/api/messages
  - POST http://localhost:3002/api/messages

### Tester le hot-reloading

1. Modifier le fichier `app.py`
2. Sauvegarder le fichier
3. Observer le rechargement automatique dans les logs Docker
4. Rafraîchir la page web pour voir les changements

### Exemple de modification

Dans `app.py`, changez le titre :
```python
<h1>🐍 Flask Guestbook MODIFIÉ <span class="python-badge">Python + Hot Reload</span></h1>
```

## Configuration Hot-Reload

Le hot-reloading est activé via :

1. **Variables d'environnement Flask** :
   - `FLASK_ENV=development`
   - `FLASK_DEBUG=1`
   - `PYTHONUNBUFFERED=1`

2. **Mode debug Flask** :
   ```python
   app.run(host='0.0.0.0', port=port, debug=True)
   ```

3. **Volume Docker** :
   ```yaml
   volumes:
     - .:/app
     - /app/__pycache__  # Exclure le cache Python
   ```

## Vérifications

- ✅ L'application se recharge automatiquement lors des modifications
- ✅ Les dépendances sont installées via `requirements.txt`
- ✅ Le conteneur redémarre rapidement après les changements
- ✅ Les logs montrent la détection des changements de fichiers
- ✅ La persistance Redis fonctionne entre les redémarrages
