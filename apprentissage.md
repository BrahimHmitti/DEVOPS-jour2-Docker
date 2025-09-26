# Apprentissages

## Problèmes rencontrés


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

- **Hot-reloading en développement** : Utilisation d'Air pour recompiler et redémarrer automatiquement l'application lors des modifications.
  - *Pourquoi utile* : Accélère le cycle de développement en évitant les étapes manuelles de compilation/redémarrage.tissages

*TESTS* on a ajouté des nouvelles valeurs dans la guestbook ensuite on a down les containers et qu'on a rebuild on a trouvé toujours les valeurs.


