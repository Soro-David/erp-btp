# BTP Manager — ERP Spécialisé BTP (Côte d'Ivoire & Afrique Francophone)

## Présentation

**BTP Manager** est un ERP métier complet conçu pour piloter le cycle intégral des projets de BTP :
> **Appel d'offres → Étude → Devis → Soumission → Contrat → Chantier → Planification → Budget → Achats → Stocks → Travaux → Équipe → Engins → Avancement → Situations de travaux → Facturation → Paiement → Réception → Bilan**

## Stack Technique

- **Backend** : FastAPI (Python 3.12), SQLAlchemy, Pydantic, Alembic
- **Base de données** : PostgreSQL 16
- **Frontend** : Vue.js 3, Vite, Pinia, Vue Router, Axios
- **Conteneurisation** : Docker & Docker Compose

## Structure du Projet

```text
erp-btp/
├── backend/                  # API REST FastAPI (Clean Architecture)
│   ├── app/
│   │   ├── api/v1/          # Endpoints de l'API
│   │   ├── core/            # Config, base de données, sécurité
│   │   ├── models/          # Entités SQLAlchemy
│   │   ├── schemas/         # Schémas Pydantic
│   │   ├── repositories/    # Accès aux données
│   │   ├── services/        # Logique métier pure
│   │   └── utils/           # Fonctions utilitaires
│   ├── alembic/             # Migrations de base de données
│   ├── tests/               # Tests unitaires et d'intégration
│   ├── requirements.txt     # Dépendances Python
│   └── Dockerfile           # Image conteneur Backend
│
├── frontend/                 # Application Vue 3 SPA
│   ├── src/
│   │   ├── assets/          # Fichiers statiques, icônes, CSS
│   │   ├── components/      # Composants réutilisables
│   │   ├── layouts/         # Layouts ERP (Sidebar, Header, etc.)
│   │   ├── views/           # Vues de chaque module
│   │   ├── router/          # Routes Vue Router
│   │   ├── stores/          # Stores Pinia
│   │   ├── services/        # Clients d'API HTTP Axios
│   │   └── composables/     # Logique composable Vue
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── Dockerfile           # Image conteneur Frontend
│
├── docker/                   # Scripts & configurations Docker auxiliaires
├── docker-compose.yml        # Définition des services (Postgres, Backend, Frontend)
├── .env.example              # Gabarit des variables d'environnement
├── .gitignore
└── README.md
```

## Démarrage Rapide

1. Cloner le dépôt et copier l'environnement :
   ```bash
   cp .env.example .env
   ```

2. Lancer les services avec Docker Compose :
   ```bash
   docker compose up -d --build
   ```

3. Accéder aux interfaces :
   - **Frontend Vue.js** : [http://localhost:5173](http://localhost:5173)
   - **Documentation API Swagger** : [http://localhost:8000/docs](http://localhost:8000/docs)
   - **Endpoint de Santé** : [http://localhost:8000/api/v1/health](http://localhost:8000/api/v1/health)
