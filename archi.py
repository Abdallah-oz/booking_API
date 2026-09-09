"""
scaffold.py
Génère la structure de dossiers/fichiers du projet Booking API.
À lancer une seule fois depuis la racine du projet (là où se trouve .venv).
"""

from pathlib import Path

# Liste des dossiers à créer
DIRECTORIES = [
    "app",
    "app/core",
    "app/db",
    "app/models",
    "app/schemas",
    "app/crud",
    "app/api",
    "app/api/v1",
    "app/services",
    "alembic/versions",
    "tests",
]

# Liste des fichiers à créer (vides pour l'instant)
FILES = [
    "app/__init__.py",
    "app/main.py",
    "app/config.py",

    "app/core/__init__.py",
    "app/core/security.py",
    "app/core/dependencies.py",
    "app/core/exceptions.py",

    "app/db/__init__.py",
    "app/db/base.py",
    "app/db/session.py",
    "app/db/init_db.py",

    "app/models/__init__.py",
    "app/models/user.py",
    "app/models/hotel.py",
    "app/models/booking.py",
    "app/models/room.py",

    "app/schemas/__init__.py",
    "app/schemas/user.py",
    "app/schemas/hotel.py",
    "app/schemas/booking.py",
    "app/schemas/token.py",

    "app/crud/__init__.py",
    "app/crud/user.py",
    "app/crud/hotel.py",
    "app/crud/booking.py",

    "app/api/__init__.py",
    "app/api/deps.py",

    "app/api/v1/__init__.py",
    "app/api/v1/router.py",
    "app/api/v1/auth.py",
    "app/api/v1/users.py",
    "app/api/v1/hotels.py",
    "app/api/v1/bookings.py",
    "app/api/v1/admin.py",

    "app/services/__init__.py",
    "app/services/booking_service.py",
    "app/services/hotel_service.py",

    "tests/__init__.py",
    "tests/conftest.py",
    "tests/test_auth.py",
    "tests/test_bookings.py",

    ".env",
    ".env.example",
    ".gitignore",
    "requirements.txt",
    "Dockerfile",
    "docker-compose.yml",
    "README.md",
]


def create_structure():
    base_path = Path(__file__).parent

    # Créer les dossiers
    for directory in DIRECTORIES:
        dir_path = base_path / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"[DIR]  {dir_path}")

    # Créer les fichiers (sans écraser s'ils existent déjà)
    for file in FILES:
        file_path = base_path / file
        if not file_path.exists():
            file_path.touch()
            print(f"[FILE] {file_path}")
        else:
            print(f"[SKIP] {file_path} (existe déjà)")

    print("\n✅ Structure créée avec succès.")


if __name__ == "__main__":
    create_structure()