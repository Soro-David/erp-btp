import sys
from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from app.core.security import hash_password


def seed_superadmin():
    """Initialise le compte SuperAdmin par défaut s'il n'existe pas encore."""
    # Créer les tables si elles ne sont pas encore créées
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        admin_email = "admin@gmail.com"
        admin_password = "Password@1234"

        existing_admin = db.query(User).filter(User.email == admin_email).first()
        if existing_admin:
            print(f"ℹ️  [SEEDER] Le compte SuperAdmin '{admin_email}' existe déjà (ID: {existing_admin.id}).")
            return

        super_admin = User(
            email=admin_email,
            hashed_password=hash_password(admin_password),
            first_name="Super",
            last_name="Admin",
            phone="+2250700000000",
            role=UserRole.SUPER_ADMIN,
            is_active=True,
        )

        db.add(super_admin)
        db.commit()
        db.refresh(super_admin)

        print("==================================================================")
        print("✅ [SEEDER] Compte SuperAdmin initialisé avec succès !")
        print(f"👉 Email       : {admin_email}")
        print(f"👉 Mot de passe: {admin_password}")
        print(f"👉 Rôle        : {super_admin.role.value}")
        print("==================================================================")

    except Exception as e:
        db.rollback()
        print(f"❌ [SEEDER] Erreur lors du seeding : {e}", file=sys.stderr)
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    seed_superadmin()
