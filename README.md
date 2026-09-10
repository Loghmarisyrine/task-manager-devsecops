# Task Manager — application de démo pour pipeline DevSecOps

Petite application Django fonctionnelle (gestion de tâches avec comptes utilisateurs),
conçue comme base pour :
- **Sujet 01** : chaîne CI/CD conteneurisée (Docker, GitHub Actions, déploiement automatique)
- **Sujet 05** : pipeline DevSecOps (SonarQube, Trivy, Gitleaks, OWASP ZAP)

## Fonctionnalités

- Inscription / connexion utilisateur
- CRUD de tâches (titre, description, priorité, statut)
- Chaque utilisateur ne voit que ses propres tâches
- Endpoint `/health/` pour les sondes de disponibilité
- Interface admin Django (`/admin/`)

## Lancer en local (sans Docker)

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optionnel
python manage.py runserver
```

Accès : http://localhost:8000

## Lancer avec Docker Compose

```bash
cp .env.example .env
# éditer .env avec de vraies valeurs (DJANGO_SECRET_KEY notamment)
docker compose up --build
```

Accès : http://localhost (via Nginx) ou http://localhost:8000 (direct Django/Gunicorn)

## Lancer les tests

```bash
python manage.py test
```

7 tests couvrent : modèle Task, vues CRUD, isolation des tâches par utilisateur,
authentification requise, endpoint de santé.

## Structure

```
taskmanager/       # config Django (settings, urls, wsgi)
tasks/              # app métier : models, views, tests, templates
Dockerfile          # image durcie (utilisateur non-root)
docker-compose.yml  # web + db (Postgres) + nginx
nginx.conf          # reverse proxy
.github/workflows/  # pipeline CI/CD (base + emplacements pour DevSecOps)
```

## Prochaines étapes (Sujet 05 — DevSecOps)

Les emplacements sont déjà commentés dans `.github/workflows/ci-cd.yml` :
1. SonarQube (analyse statique + quality gate)
2. Gitleaks (détection de secrets dans l'historique Git)
3. Trivy (scan de l'image Docker et des dépendances)
4. OWASP ZAP (scan dynamique sur l'environnement de staging)
