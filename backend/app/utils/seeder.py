import sys
from app.core.database import SessionLocal, Base, engine
from app.models.user import User, UserRole
from datetime import date, timedelta, datetime
from app.models.chantier import ChantierType, Client, Responsable, Chantier
from app.models.task import Phase, Task, TaskDependency, Milestone
from app.models.purchase import (
    Supplier,
    MaterialCategory,
    MaterialUnit,
    Material,
    StockLocation,
    Purchase,
    PurchaseLine,
    PurchaseReceipt,
    PurchaseReceiptItem,
    StockMovement,
)
from app.services.task import TaskService
from app.core.security import hash_password


def seed_planning_and_tasks(db):
    """Initialise des phases, tâches, sous-tâches, dépendances et jalons réalistes pour le Chantier 1."""
    chantier = db.query(Chantier).first()
    if not chantier:
        print("ℹ️  [SEEDER] Aucun chantier trouvé pour initialiser le planning.")
        return

    # Vérifier si des tâches existent déjà
    if db.query(Task).filter(Task.chantier_id == chantier.id).count() > 0:
        print("ℹ️  [SEEDER] Le planning et les tâches du chantier 1 sont déjà initialisés.")
        return

    responsables = db.query(Responsable).all()
    resp_chef = responsables[0].id if len(responsables) > 0 else None
    resp_conducteur = responsables[1].id if len(responsables) > 1 else resp_chef
    resp_ch = responsables[2].id if len(responsables) > 2 else resp_chef

    today = date.today()

    # 1. Création des Phases
    phase_data = [
        {"code": "PHS-01", "name": "Études & Travaux Préparatoires", "display_order": 1, "status": "Terminée", "progress": 100.0, "start_date_planned": today - timedelta(days=60), "end_date_planned": today - timedelta(days=40), "responsible_id": resp_chef},
        {"code": "PHS-02", "name": "Fondations & Terrassement", "display_order": 2, "status": "Terminée", "progress": 100.0, "start_date_planned": today - timedelta(days=39), "end_date_planned": today - timedelta(days=15), "responsible_id": resp_conducteur},
        {"code": "PHS-03", "name": "Gros Œuvre & Structure R+8", "display_order": 3, "status": "En cours", "progress": 55.0, "start_date_planned": today - timedelta(days=14), "end_date_planned": today + timedelta(days=45), "responsible_id": resp_ch},
        {"code": "PHS-04", "name": "Corps d'état secondaires & MEP", "display_order": 4, "status": "En attente", "progress": 10.0, "start_date_planned": today + timedelta(days=30), "end_date_planned": today + timedelta(days=80), "responsible_id": resp_conducteur},
        {"code": "PHS-05", "name": "Finitions & Réception", "display_order": 5, "status": "À faire", "progress": 0.0, "start_date_planned": today + timedelta(days=81), "end_date_planned": today + timedelta(days=120), "responsible_id": resp_chef},
    ]

    phases = {}
    for p in phase_data:
        phase_obj = Phase(chantier_id=chantier.id, **p)
        db.add(phase_obj)
        db.flush()
        phases[p["code"]] = phase_obj

    # 2. Création des Tâches Mères et Sous-tâches
    # Phase 1
    t1 = Task(
        code="TSK-2026-001", name="Étude géotechnique de sol G2 et levé topographique",
        chantier_id=chantier.id, phase_id=phases["PHS-01"].id, responsible_id=resp_chef,
        status="Terminée", priority="Normale", progress=100.0, weight=1.0,
        planned_start_date=today - timedelta(days=60), planned_end_date=today - timedelta(days=50),
        estimated_duration_days=11, actual_start_date=today - timedelta(days=60), actual_end_date=today - timedelta(days=50),
        team_name="Équipe Géotechnique", workers_count=4
    )
    t2 = Task(
        code="TSK-2026-002", name="Installation base-vie, clôture et raccordements chantier",
        chantier_id=chantier.id, phase_id=phases["PHS-01"].id, responsible_id=resp_conducteur,
        status="Terminée", priority="Normale", progress=100.0, weight=1.0,
        planned_start_date=today - timedelta(days=49), planned_end_date=today - timedelta(days=40),
        estimated_duration_days=10, actual_start_date=today - timedelta(days=49), actual_end_date=today - timedelta(days=40),
        team_name="Installation", workers_count=6
    )
    db.add_all([t1, t2])
    db.flush()

    # Phase 2
    t3 = Task(
        code="TSK-2026-003", name="Terrassement général & Fouilles en excavation",
        chantier_id=chantier.id, phase_id=phases["PHS-02"].id, responsible_id=resp_ch,
        status="Terminée", priority="Importante", progress=100.0, weight=1.5,
        planned_start_date=today - timedelta(days=39), planned_end_date=today - timedelta(days=25),
        estimated_duration_days=15, actual_start_date=today - timedelta(days=39), actual_end_date=today - timedelta(days=25),
        equipment="Pelleteuse 25T, 3 Camions bennes", workers_count=8
    )
    db.add(t3)
    db.flush()

    sub_t3_1 = Task(
        code="TSK-2026-004", name="Fouilles en rigoles et puits de fondation",
        chantier_id=chantier.id, phase_id=phases["PHS-02"].id, parent_task_id=t3.id, responsible_id=resp_ch,
        status="Terminée", priority="Normale", progress=100.0, weight=1.0,
        planned_start_date=today - timedelta(days=39), planned_end_date=today - timedelta(days=32),
        estimated_duration_days=8, actual_start_date=today - timedelta(days=39), actual_end_date=today - timedelta(days=32),
        workers_count=4
    )
    sub_t3_2 = Task(
        code="TSK-2026-005", name="Évacuation des déblais et compactage fond de forme",
        chantier_id=chantier.id, phase_id=phases["PHS-02"].id, parent_task_id=t3.id, responsible_id=resp_ch,
        status="Terminée", priority="Normale", progress=100.0, weight=1.0,
        planned_start_date=today - timedelta(days=31), planned_end_date=today - timedelta(days=25),
        estimated_duration_days=7, actual_start_date=today - timedelta(days=31), actual_end_date=today - timedelta(days=25),
        workers_count=4
    )
    db.add_all([sub_t3_1, sub_t3_2])

    t6 = Task(
        code="TSK-2026-006", name="Ferraillage et coulage des semelles et longrines",
        chantier_id=chantier.id, phase_id=phases["PHS-02"].id, responsible_id=resp_conducteur,
        status="Terminée", priority="Critique", progress=100.0, weight=2.0,
        planned_start_date=today - timedelta(days=24), planned_end_date=today - timedelta(days=15),
        estimated_duration_days=10, actual_start_date=today - timedelta(days=24), actual_end_date=today - timedelta(days=15),
        materials="Béton C30/37 (180 m3), Acier HA FeE500 (15 tonnes)", workers_count=14
    )
    db.add(t6)
    db.flush()

    # Phase 3
    t7 = Task(
        code="TSK-2026-007", name="Élévation structure RDC à R+3 (Poteaux & Dalles)",
        chantier_id=chantier.id, phase_id=phases["PHS-03"].id, responsible_id=resp_conducteur,
        status="Terminée", priority="Critique", progress=100.0, weight=2.5,
        planned_start_date=today - timedelta(days=14), planned_end_date=today - timedelta(days=1),
        estimated_duration_days=14, actual_start_date=today - timedelta(days=14), actual_end_date=today - timedelta(days=1),
        equipment="Grue à tour 45m, Centrale à béton", workers_count=20
    )
    db.add(t7)
    db.flush()

    t8 = Task(
        code="TSK-2026-008", name="Élévation structure R+4 à R+8",
        chantier_id=chantier.id, phase_id=phases["PHS-03"].id, responsible_id=resp_ch,
        status="En cours", priority="Critique", progress=40.0, weight=3.0,
        planned_start_date=today, planned_end_date=today + timedelta(days=35),
        estimated_duration_days=36, actual_start_date=today,
        equipment="Grue à tour", workers_count=18
    )
    db.add(t8)
    db.flush()

    sub_t8_1 = Task(
        code="TSK-2026-009", name="Coffrage et ferraillage dalle plancher R+5",
        chantier_id=chantier.id, phase_id=phases["PHS-03"].id, parent_task_id=t8.id, responsible_id=resp_ch,
        status="En cours", priority="Importante", progress=75.0, weight=1.0,
        planned_start_date=today, planned_end_date=today + timedelta(days=8),
        estimated_duration_days=9, actual_start_date=today, workers_count=10
    )
    sub_t8_2 = Task(
        code="TSK-2026-010", name="Coulage béton et élévation poteaux R+6",
        chantier_id=chantier.id, phase_id=phases["PHS-03"].id, parent_task_id=t8.id, responsible_id=resp_ch,
        status="À faire", priority="Normale", progress=0.0, weight=1.0,
        planned_start_date=today + timedelta(days=9), planned_end_date=today + timedelta(days=20),
        estimated_duration_days=12, workers_count=10
    )
    db.add_all([sub_t8_1, sub_t8_2])

    # Phase 4 (with blocked task example)
    t11 = Task(
        code="TSK-2026-011", name="Passage gaines CFO/CFA et plomberie RDC-R+2",
        chantier_id=chantier.id, phase_id=phases["PHS-04"].id, responsible_id=resp_conducteur,
        status="Bloquée", priority="Importante", progress=25.0, weight=1.5,
        planned_start_date=today - timedelta(days=5), planned_end_date=today + timedelta(days=15),
        estimated_duration_days=21, actual_start_date=today - timedelta(days=5),
        is_blocked=True, blocking_reason="Attente livraison chemins de câbles et colonnes montantes",
        blocking_date=today - timedelta(days=2), blocking_impact="Retard possible sur le second œuvre",
        blocking_comment="Fournisseur en rupture, livraison confirmée sous 48h.",
        workers_count=6
    )
    t12 = Task(
        code="TSK-2026-012", name="Installation ventilation mécanique et climatisation",
        chantier_id=chantier.id, phase_id=phases["PHS-04"].id, responsible_id=resp_conducteur,
        status="À faire", priority="Normale", progress=0.0, weight=1.0,
        planned_start_date=today + timedelta(days=16), planned_end_date=today + timedelta(days=40),
        estimated_duration_days=25, workers_count=6
    )
    db.add_all([t11, t12])

    # Phase 5
    t13 = Task(
        code="TSK-2026-013", name="Pose carrelage, faïences et peintures",
        chantier_id=chantier.id, phase_id=phases["PHS-05"].id, responsible_id=resp_conducteur,
        status="À faire", priority="Faible", progress=0.0, weight=2.0,
        planned_start_date=today + timedelta(days=50), planned_end_date=today + timedelta(days=100),
        estimated_duration_days=51, workers_count=12
    )
    db.add(t13)
    db.flush()

    # 3. Dépendances Fin -> Début
    deps = [
        TaskDependency(predecessor_id=t1.id, successor_id=t3.id, dependency_type="FINISH_TO_START", lag_days=0),
        TaskDependency(predecessor_id=t3.id, successor_id=t6.id, dependency_type="FINISH_TO_START", lag_days=0),
        TaskDependency(predecessor_id=t6.id, successor_id=t7.id, dependency_type="FINISH_TO_START", lag_days=0),
        TaskDependency(predecessor_id=t7.id, successor_id=t8.id, dependency_type="FINISH_TO_START", lag_days=0),
        TaskDependency(predecessor_id=t7.id, successor_id=t11.id, dependency_type="FINISH_TO_START", lag_days=0),
        TaskDependency(predecessor_id=t11.id, successor_id=t12.id, dependency_type="FINISH_TO_START", lag_days=0),
        TaskDependency(predecessor_id=t12.id, successor_id=t13.id, dependency_type="FINISH_TO_START", lag_days=0),
    ]
    db.add_all(deps)

    # 4. Jalons (Milestones)
    milestones = [
        Milestone(code="JAL-01", name="Validation Études Géotechniques & PIC", chantier_id=chantier.id, responsible_id=resp_chef, planned_date=today - timedelta(days=40), actual_date=today - timedelta(days=40), status="Atteint"),
        Milestone(code="JAL-02", name="Achèvement Fondations & Semelles", chantier_id=chantier.id, responsible_id=resp_conducteur, planned_date=today - timedelta(days=15), actual_date=today - timedelta(days=15), status="Atteint"),
        Milestone(code="JAL-03", name="Achèvement Gros Œuvre R+8 (Hors d'eau)", chantier_id=chantier.id, responsible_id=resp_ch, planned_date=today + timedelta(days=35), status="À venir"),
        Milestone(code="JAL-04", name="Clôture des Corps d'État Secondaires", chantier_id=chantier.id, responsible_id=resp_conducteur, planned_date=today + timedelta(days=80), status="À venir"),
        Milestone(code="JAL-05", name="Réception Provisoire des Travaux (RPT)", chantier_id=chantier.id, responsible_id=resp_chef, planned_date=today + timedelta(days=120), status="À venir"),
    ]
    db.add_all(milestones)
    db.commit()

    # Recalculer l'avancement global
    service = TaskService(db)
    global_p = service.recalculate_chantier_progress(chantier.id)
    print(f"✅ [SEEDER] Planning initialisé : 5 phases, 13 tâches/sous-tâches, 7 dépendances, 5 jalons. Avancement global: {global_p}%")


def seed_superadmin(db):
    """Initialise le compte SuperAdmin par défaut s'il n'existe pas encore."""
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


def seed_chantier_types(db):
    """Initialise les types de chantier référentiels de base."""
    types_data = [
        {"name": "Construction", "description": "Construction neuve de bâtiments, villas ou immeubles"},
        {"name": "Réhabilitation", "description": "Travaux de rénovation, renforcement ou réhabilitation"},
        {"name": "Route", "description": "Voiries, bitumage, pistes et réseaux divers (VRD)"},
        {"name": "Bâtiment administratif", "description": "Écoles, ministères, mairies, hôpitaux"},
        {"name": "Logement", "description": "Programmes immobiliers, résidences et logements sociaux"},
        {"name": "Ouvrage d'art", "description": "Ponts, passerelles, échangeurs, viaducs"},
        {"name": "Infrastructure", "description": "Adduction d'eau, stations d'épuration, lignes électriques"},
        {"name": "Autre", "description": "Autres types d'aménagements et travaux spécifiques"},
    ]

    added = 0
    for t in types_data:
        exists = db.query(ChantierType).filter(ChantierType.name == t["name"]).first()
        if not exists:
            db.add(ChantierType(name=t["name"], description=t["description"], is_active=True))
            added += 1

    if added > 0:
        db.commit()
        print(f"✅ [SEEDER] {added} types de chantiers initialisés.")
    else:
        print("ℹ️  [SEEDER] Types de chantiers déjà initialisés.")


def seed_responsables(db):
    """Initialise des profils d'intervenants types."""
    responsables_data = [
        {"first_name": "Konan", "last_name": "Kouassi", "role_name": "Chef de projet", "phone": "+225 07 11 22 33", "email": "k.kouassi@btp.ci", "company": "BTP Manager"},
        {"first_name": "Jean-Paul", "last_name": "Koffi", "role_name": "Conducteur des travaux", "phone": "+225 05 44 55 66", "email": "jp.koffi@btp.ci", "company": "BTP Manager"},
        {"first_name": "Amadou", "last_name": "Traoré", "role_name": "Chef de chantier", "phone": "+225 01 77 88 99", "email": "a.traore@btp.ci", "company": "SOGEA BTP"},
        {"first_name": "Salimata", "last_name": "Diarra", "role_name": "Responsable HSE", "phone": "+225 07 99 00 11", "email": "s.diarra@btp.ci", "company": "HSE Sécurité Plus"},
        {"first_name": "Bureau d'Études", "last_name": "Structure CI", "role_name": "Bureau d'études", "phone": "+225 27 22 44 11", "email": "contact@structure-ci.com", "company": "Cabinet Structure CI"},
        {"first_name": "Société Ivoirienne", "last_name": "Terrassement", "role_name": "Entreprise exécutante", "phone": "+225 27 20 30 40", "email": "direction@sit-btp.ci", "company": "SIT BTP"},
    ]

    added = 0
    for r in responsables_data:
        exists = db.query(Responsable).filter(
            Responsable.first_name == r["first_name"],
            Responsable.last_name == r["last_name"]
        ).first()
        if not exists:
            db.add(Responsable(**r, is_active=True))
            added += 1

    if added > 0:
        db.commit()
        print(f"✅ [SEEDER] {added} responsables/intervenants types initialisés.")
    else:
        print("ℹ️  [SEEDER] Responsables déjà initialisés.")


def seed_clients(db):
    """Initialise des clients types."""
    clients_data = [
        {
            "type": "Administration publique",
            "name": "Mairie de Yopougon / Ministère Éducation",
            "phone": "+225 27 23 45 67",
            "email": "marches@yopougon.ci",
            "address": "Mairie Centrale, Yopougon, Abidjan",
            "contact_person": "M. Coulibaly I.",
            "ministry": "Ministère de l'Éducation Nationale",
            "direction": "Direction des Infrastructures Scolaires",
            "service": "Service des Marchés Publics",
            "admin_in_charge": "M. Coulibaly Ibrahim",
        },
        {
            "type": "Entreprise",
            "name": "SCI Laguna Immobilier",
            "phone": "+225 27 22 55 88",
            "email": "contact@scilaguna.ci",
            "address": "Boulevard Lagunaire, Plateau, Abidjan",
            "contact_person": "Mme Bamba A.",
            "company_name": "SCI Laguna SARL",
            "rccm": "CI-ABJ-2023-B-14285",
            "company_contact": "+225 07 48 55 66",
        },
        {
            "type": "Particulier",
            "name": "M. Albert Koffi",
            "phone": "+225 07 08 09 10",
            "email": "albert.koffi@gmail.com",
            "address": "Riviera Golf, Cocody, Abidjan",
            "contact_person": "M. Albert Koffi",
        }
    ]

    added = 0
    for c in clients_data:
        exists = db.query(Client).filter(Client.name == c["name"]).first()
        if not exists:
            db.add(Client(**c))
            added += 1

    if added > 0:
        db.commit()
        print(f"✅ [SEEDER] {added} clients types initialisés.")
    else:
        print("ℹ️  [SEEDER] Clients déjà initialisés.")


def seed_purchases_and_stocks(db):
    """Initialise les fournisseurs, catégories, unités, matériaux, dépôts et achats de test."""
    if db.query(Supplier).count() > 0:
        print("ℹ️  [SEEDER] Le module Achats & Stocks est déjà initialisé.")
        return

    print("🚀 [SEEDER] Initialisation du module Achats & Stocks...")

    # 1. Fournisseurs ivoiriens
    suppliers_data = [
        {
            "code": "FOUR-001",
            "name": "CIMAF Côte d'Ivoire",
            "trade_name": "Ciments de l'Afrique",
            "contact_name": "M. Kouadio Jean",
            "phone": "+225 27 23 51 00",
            "email": "commandes@cimaf.ci",
            "address": "Zone Industrielle de Yopougon",
            "city": "Abidjan",
            "country": "Côte d'Ivoire",
            "rccm": "CI-ABJ-2011-B-3490",
            "ncc": "1103490P",
            "payment_terms": "30 jours fin de mois",
            "notes": "Fournisseur principal de ciment CPJ 35 et CPJ 45.",
        },
        {
            "code": "FOUR-002",
            "name": "SMCI - Société Métallurgique de Côte d'Ivoire",
            "trade_name": "SMCI Armatures",
            "contact_name": "Mme Bamba Fatou",
            "phone": "+225 27 21 24 55",
            "email": "ventes@smci-ci.com",
            "address": "Zone Industrielle de Vridi",
            "city": "Abidjan",
            "country": "Côte d'Ivoire",
            "rccm": "CI-ABJ-1998-B-1284",
            "ncc": "9812840M",
            "payment_terms": "Paiement à la livraison",
            "notes": "Aciers haute adhérence FeE500 tous diamètres, treillis soudés.",
        },
        {
            "code": "FOUR-003",
            "name": "Granulats & Carrières d'Abidjan - SATP",
            "trade_name": "SATP Carrières",
            "contact_name": "M. Traoré Adama",
            "phone": "+225 07 48 99 22",
            "email": "contact@satp-ci.com",
            "address": "Route de Bassam, Port-Bouët",
            "city": "Abidjan",
            "country": "Côte d'Ivoire",
            "rccm": "CI-ABJ-2005-B-4521",
            "ncc": "0545210K",
            "payment_terms": "Comptant ou virement 15j",
            "notes": "Sable lagunaire lavé, graviers concassés 5/15, 15/25.",
        },
        {
            "code": "FOUR-004",
            "name": "Bernabé Côte d'Ivoire",
            "trade_name": "Bernabé Matériaux & Outillage",
            "contact_name": "M. Diop Mamadou",
            "phone": "+225 27 21 21 34",
            "email": "service.client@bernabe.ci",
            "address": "Boulevard de Marseille, Treichville",
            "city": "Abidjan",
            "country": "Côte d'Ivoire",
            "rccm": "CI-ABJ-1960-B-0210",
            "ncc": "6002100A",
            "payment_terms": "45 jours fin de mois",
            "notes": "Quincaillerie professionnelle, outillage, équipement de chantier.",
        },
        {
            "code": "FOUR-005",
            "name": "BatiPlus Côte d'Ivoire",
            "trade_name": "BatiPlus Abidjan",
            "contact_name": "M. Sanogo Ali",
            "phone": "+225 27 21 35 88",
            "email": "commercial@batiplus.ci",
            "address": "Boulevard VGE, Marcory",
            "city": "Abidjan",
            "country": "Côte d'Ivoire",
            "rccm": "CI-ABJ-2014-B-8921",
            "ncc": "1489210Z",
            "payment_terms": "30 jours",
            "notes": "Bois de coffrage, tuyauterie PVC, étanchéité.",
        },
    ]

    suppliers_dict = {}
    for sup_data in suppliers_data:
        sup = Supplier(**sup_data)
        db.add(sup)
        db.flush()
        suppliers_dict[sup.code] = sup

    # 2. Catégories de Matériaux
    categories_data = [
        {"code": "CAT-GROS_OEUVRE", "name": "Gros Œuvre", "description": "Matériaux lourds de structure et fondations"},
        {"code": "CAT-CIMENT", "name": "Liants & Ciments", "description": "Ciments normalisés, chaux, mortiers prêts"},
        {"code": "CAT-ACIERS", "name": "Aciers & Armatures", "description": "Fers à béton, treillis, fils de ligature"},
        {"code": "CAT-GRANULATS", "name": "Granulats & Sables", "description": "Sable lagunaire, graviers concassés"},
        {"code": "CAT-BOIS", "name": "Bois & Coffrage", "description": "Madriers, planches de coffrage, chevrons"},
        {"code": "CAT-PLOMB", "name": "Plomberie & Réseaux", "description": "Tubes PVC, raccords, évacuation"},
        {"code": "CAT-ELEC", "name": "Électricité & Câblage", "description": "Câbles, gaines, tableaux électriques"},
        {"code": "CAT-QUINCAIL", "name": "Quincaillerie & Outillage", "description": "Clous, vis, disques, EPI"},
    ]

    cat_dict = {}
    for c_data in categories_data:
        c = MaterialCategory(**c_data)
        db.add(c)
        db.flush()
        cat_dict[c.code] = c

    # 3. Unités de Mesure
    units_data = [
        {"code": "SAC", "name": "Sac de 50 kg"},
        {"code": "T", "name": "Tonne"},
        {"code": "BARRE", "name": "Barre de 12 mètres"},
        {"code": "M3", "name": "Mètre cube"},
        {"code": "U", "name": "Unité / Pièce"},
        {"code": "ROULEAU", "name": "Rouleau"},
        {"code": "KG", "name": "Kilogramme"},
        {"code": "M2", "name": "Mètre carré"},
    ]

    unit_dict = {}
    for u_data in units_data:
        u = MaterialUnit(**u_data)
        db.add(u)
        db.flush()
        unit_dict[u.code] = u

    # 4. Matériaux
    materials_data = [
        {
            "code": "MAT-2026-001",
            "name": "Ciment CPJ 35 (Sac 50kg)",
            "description": "Ciment Portland composé conforme norme ivoirienne NI",
            "category_id": cat_dict["CAT-CIMENT"].id,
            "unit_id": unit_dict["SAC"].id,
            "reference": "CIM-CPJ35",
            "indicative_price": 4800.0,
            "minimum_stock": 100.0,
            "maximum_stock": 1500.0,
        },
        {
            "code": "MAT-2026-002",
            "name": "Ciment CPJ 45 Haute Résistance (Sac 50kg)",
            "description": "Ciment pour béton précontraint et hautes résistances initiales",
            "category_id": cat_dict["CAT-CIMENT"].id,
            "unit_id": unit_dict["SAC"].id,
            "reference": "CIM-CPJ45",
            "indicative_price": 5400.0,
            "minimum_stock": 50.0,
            "maximum_stock": 800.0,
        },
        {
            "code": "MAT-2026-003",
            "name": "Fer à béton HA FeE500 Ø8 (Barre 12m)",
            "description": "Acier haute adhérence pour armatures et étriers",
            "category_id": cat_dict["CAT-ACIERS"].id,
            "unit_id": unit_dict["BARRE"].id,
            "reference": "ACIER-HA08",
            "indicative_price": 3600.0,
            "minimum_stock": 150.0,
            "maximum_stock": 2000.0,
        },
        {
            "code": "MAT-2026-004",
            "name": "Fer à béton HA FeE500 Ø10 (Barre 12m)",
            "description": "Acier haute adhérence pour poteaux et poutres",
            "category_id": cat_dict["CAT-ACIERS"].id,
            "unit_id": unit_dict["BARRE"].id,
            "reference": "ACIER-HA10",
            "indicative_price": 5700.0,
            "minimum_stock": 100.0,
            "maximum_stock": 1500.0,
        },
        {
            "code": "MAT-2026-005",
            "name": "Fer à béton HA FeE500 Ø12 (Barre 12m)",
            "description": "Acier haute adhérence pour semelles et voiles",
            "category_id": cat_dict["CAT-ACIERS"].id,
            "unit_id": unit_dict["BARRE"].id,
            "reference": "ACIER-HA12",
            "indicative_price": 8200.0,
            "minimum_stock": 80.0,
            "maximum_stock": 1000.0,
        },
        {
            "code": "MAT-2026-006",
            "name": "Sable lagunaire lavé 0/4",
            "description": "Sable propre pour maçonnerie et béton fin",
            "category_id": cat_dict["CAT-GRANULATS"].id,
            "unit_id": unit_dict["M3"].id,
            "reference": "SAB-LAG04",
            "indicative_price": 14000.0,
            "minimum_stock": 20.0,
            "maximum_stock": 200.0,
        },
        {
            "code": "MAT-2026-007",
            "name": "Gravier concassé 15/25",
            "description": "Gravillon de carrière pour béton armé de structure",
            "category_id": cat_dict["CAT-GRANULATS"].id,
            "unit_id": unit_dict["M3"].id,
            "reference": "GRAV-1525",
            "indicative_price": 19500.0,
            "minimum_stock": 30.0,
            "maximum_stock": 300.0,
        },
        {
            "code": "MAT-2026-008",
            "name": "Madrier bois blanc 7x15x400 cm",
            "description": "Bois pour étaiement et structure de coffrage",
            "category_id": cat_dict["CAT-BOIS"].id,
            "unit_id": unit_dict["U"].id,
            "reference": "BOIS-MAD715",
            "indicative_price": 4200.0,
            "minimum_stock": 50.0,
            "maximum_stock": 500.0,
        },
        {
            "code": "MAT-2026-009",
            "name": "Planche de coffrage 2.5x20x400 cm",
            "description": "Planche en bois blanc raboté 1 face pour parements",
            "category_id": cat_dict["CAT-BOIS"].id,
            "unit_id": unit_dict["U"].id,
            "reference": "BOIS-PL2520",
            "indicative_price": 2800.0,
            "minimum_stock": 80.0,
            "maximum_stock": 800.0,
        },
        {
            "code": "MAT-2026-010",
            "name": "Tube PVC Pression Ø100 (Barre 4m)",
            "description": "Tubes d'évacuation eaux usées et pluviales",
            "category_id": cat_dict["CAT-PLOMB"].id,
            "unit_id": unit_dict["U"].id,
            "reference": "PVC-PRES100",
            "indicative_price": 6500.0,
            "minimum_stock": 25.0,
            "maximum_stock": 250.0,
        },
        {
            "code": "MAT-2026-011",
            "name": "Câble électrique TH 2.5mm² (Rouleau 100m)",
            "description": "Fil rigide cuivre pour circuits prises et force",
            "category_id": cat_dict["CAT-ELEC"].id,
            "unit_id": unit_dict["ROULEAU"].id,
            "reference": "ELEC-TH25",
            "indicative_price": 28000.0,
            "minimum_stock": 10.0,
            "maximum_stock": 100.0,
        },
    ]

    mat_dict = {}
    for m_data in materials_data:
        m = Material(**m_data)
        db.add(m)
        db.flush()
        mat_dict[m.code] = m

    # 5. Dépôts / Emplacements
    locations_data = [
        {
            "code": "DEP-01",
            "name": "Dépôt Central Yopougon",
            "location": "Zone Industrielle Yopougon, Abidjan",
            "type": "Dépôt principal",
            "is_active": True,
        },
        {
            "code": "DEP-02",
            "name": "Magasin Chantier Plateau",
            "location": "Résidence Les Perles du Plateau R+8",
            "type": "Magasin",
            "is_active": True,
        },
        {
            "code": "DEP-03",
            "name": "Entrepôt Matériaux Yamoussoukro",
            "location": "Quartier Morofe, Yamoussoukro",
            "type": "Entrepôt",
            "is_active": True,
        },
    ]

    loc_dict = {}
    for l_data in locations_data:
        loc = StockLocation(**l_data)
        db.add(loc)
        db.flush()
        loc_dict[loc.code] = loc

    # 6. Achats et mouvements initiaux (rattachés au Chantier 1 et ses Tâches)
    chantier = db.query(Chantier).first()
    if chantier:
        tasks = db.query(Task).filter(Task.chantier_id == chantier.id).all()
        task_1 = tasks[0] if len(tasks) > 0 else None
        task_2 = tasks[1] if len(tasks) > 1 else None

        today = date.today()

        # Commande 1: Ciments CIMAF (Reçu et mis en stock DEP-01)
        p1 = Purchase(
            reference="ACH-2026-00001",
            supplier_id=suppliers_dict["FOUR-001"].id,
            chantier_id=chantier.id,
            task_id=task_1.id if task_1 else None,
            date=today - timedelta(days=15),
            status="Reçu",
            payment_status="Payé",
            payment_mode="Virement",
            subject="Approvisionnement Ciment pour fondations et semelles",
            notes="Livraison directe sur base centrale avec déchargement.",
            total_amount=1230000.0,
            currency="FCFA",
            is_quick_purchase=False,
        )
        db.add(p1)
        db.flush()

        l1 = PurchaseLine(
            purchase_id=p1.id,
            material_id=mat_dict["MAT-2026-001"].id,
            quantity=200.0,
            unit_price=4800.0,
            total_price=960000.0,
            quantity_received=200.0,
        )
        l2 = PurchaseLine(
            purchase_id=p1.id,
            material_id=mat_dict["MAT-2026-002"].id,
            quantity=50.0,
            unit_price=5400.0,
            total_price=270000.0,
            quantity_received=50.0,
        )
        db.add_all([l1, l2])
        db.flush()

        # Réception Commande 1
        rec1 = PurchaseReceipt(
            purchase_id=p1.id,
            receipt_number="REC-2026-00001",
            date=today - timedelta(days=14),
            location_id=loc_dict["DEP-01"].id,
            notes="Réception intégrale conforme sans avaries.",
        )
        db.add(rec1)
        db.flush()

        db.add(PurchaseReceiptItem(
            receipt_id=rec1.id, purchase_line_id=l1.id, material_id=l1.material_id,
            quantity_received=200.0, quantity_rejected=0.0
        ))
        db.add(PurchaseReceiptItem(
            receipt_id=rec1.id, purchase_line_id=l2.id, material_id=l2.material_id,
            quantity_received=50.0, quantity_rejected=0.0
        ))

        # Entrées en stock correspondantes
        m1 = StockMovement(
            reference="MVT-2026-00001",
            material_id=mat_dict["MAT-2026-001"].id,
            location_id=loc_dict["DEP-01"].id,
            movement_type="Entrée",
            quantity=200.0,
            unit_price=4800.0,
            chantier_id=chantier.id,
            task_id=task_1.id if task_1 else None,
            purchase_id=p1.id,
            date=datetime.now() - timedelta(days=14),
            reason="Réception ACH-2026-00001",
        )
        m2 = StockMovement(
            reference="MVT-2026-00002",
            material_id=mat_dict["MAT-2026-002"].id,
            location_id=loc_dict["DEP-01"].id,
            movement_type="Entrée",
            quantity=50.0,
            unit_price=5400.0,
            chantier_id=chantier.id,
            task_id=task_1.id if task_1 else None,
            purchase_id=p1.id,
            date=datetime.now() - timedelta(days=14),
            reason="Réception ACH-2026-00001",
        )
        db.add_all([m1, m2])

        # Commande 2: Fers à béton SMCI (Reçu)
        p2 = Purchase(
            reference="ACH-2026-00002",
            supplier_id=suppliers_dict["FOUR-002"].id,
            chantier_id=chantier.id,
            task_id=task_2.id if task_2 else None,
            date=today - timedelta(days=10),
            status="Reçu",
            payment_status="Partiellement payé",
            payment_mode="Virement",
            subject="Armatures métalliques pour ferraillage semelles & amorces poteaux",
            notes="Acompte 50% versé à la commande, solde à 30 jours.",
            total_amount=2370000.0,
            currency="FCFA",
            is_quick_purchase=False,
        )
        db.add(p2)
        db.flush()

        l3 = PurchaseLine(
            purchase_id=p2.id,
            material_id=mat_dict["MAT-2026-004"].id,
            quantity=200.0,
            unit_price=5700.0,
            total_price=1140000.0,
            quantity_received=200.0,
        )
        l4 = PurchaseLine(
            purchase_id=p2.id,
            material_id=mat_dict["MAT-2026-005"].id,
            quantity=150.0,
            unit_price=8200.0,
            total_price=1230000.0,
            quantity_received=150.0,
        )
        db.add_all([l3, l4])
        db.flush()

        # Réception Commande 2
        rec2 = PurchaseReceipt(
            purchase_id=p2.id,
            receipt_number="REC-2026-00002",
            date=today - timedelta(days=9),
            location_id=loc_dict["DEP-01"].id,
            notes="Contrôle diamètre et qualité conforme.",
        )
        db.add(rec2)
        db.flush()

        db.add(PurchaseReceiptItem(
            receipt_id=rec2.id, purchase_line_id=l3.id, material_id=l3.material_id,
            quantity_received=200.0, quantity_rejected=0.0
        ))
        db.add(PurchaseReceiptItem(
            receipt_id=rec2.id, purchase_line_id=l4.id, material_id=l4.material_id,
            quantity_received=150.0, quantity_rejected=0.0
        ))

        # Entrées en stock Commande 2
        m3 = StockMovement(
            reference="MVT-2026-00003",
            material_id=mat_dict["MAT-2026-004"].id,
            location_id=loc_dict["DEP-01"].id,
            movement_type="Entrée",
            quantity=200.0,
            unit_price=5700.0,
            chantier_id=chantier.id,
            task_id=task_2.id if task_2 else None,
            purchase_id=p2.id,
            date=datetime.now() - timedelta(days=9),
            reason="Réception ACH-2026-00002",
        )
        m4 = StockMovement(
            reference="MVT-2026-00004",
            material_id=mat_dict["MAT-2026-005"].id,
            location_id=loc_dict["DEP-01"].id,
            movement_type="Entrée",
            quantity=150.0,
            unit_price=8200.0,
            chantier_id=chantier.id,
            task_id=task_2.id if task_2 else None,
            purchase_id=p2.id,
            date=datetime.now() - timedelta(days=9),
            reason="Réception ACH-2026-00002",
        )
        db.add_all([m3, m4])

        # Sorties de stock vers Chantier 1 (Consommation réelle sur les tâches)
        m5 = StockMovement(
            reference="MVT-2026-00005",
            material_id=mat_dict["MAT-2026-001"].id,
            location_id=loc_dict["DEP-01"].id,
            movement_type="Sortie",
            quantity=75.0,
            unit_price=4800.0,
            chantier_id=chantier.id,
            task_id=task_1.id if task_1 else None,
            date=datetime.now() - timedelta(days=6),
            reason="Bétonnage semelles isolées axe A-D",
        )
        m6 = StockMovement(
            reference="MVT-2026-00006",
            material_id=mat_dict["MAT-2026-004"].id,
            location_id=loc_dict["DEP-01"].id,
            movement_type="Sortie",
            quantity=60.0,
            unit_price=5700.0,
            chantier_id=chantier.id,
            task_id=task_2.id if task_2 else None,
            date=datetime.now() - timedelta(days=5),
            reason="Ferraillage amorces poteaux RDC",
        )
        db.add_all([m5, m6])

        # Commande 3: Granulats SATP (Commandé, en attente de livraison)
        p3 = Purchase(
            reference="ACH-2026-00003",
            supplier_id=suppliers_dict["FOUR-003"].id,
            chantier_id=chantier.id,
            date=today - timedelta(days=2),
            status="Commandé",
            payment_status="Non payé",
            payment_mode="Virement",
            subject="Fourniture de sable et gravier concassé",
            notes="Livraison planifiée par camions bennes de 20m3.",
            total_amount=1395000.0,
            currency="FCFA",
            is_quick_purchase=False,
        )
        db.add(p3)
        db.flush()

        l5 = PurchaseLine(
            purchase_id=p3.id,
            material_id=mat_dict["MAT-2026-006"].id,
            quantity=30.0,
            unit_price=14000.0,
            total_price=420000.0,
            quantity_received=0.0,
        )
        l6 = PurchaseLine(
            purchase_id=p3.id,
            material_id=mat_dict["MAT-2026-007"].id,
            quantity=50.0,
            unit_price=19500.0,
            total_price=975000.0,
            quantity_received=0.0,
        )
        db.add_all([l5, l6])

        # Achat rapide terrain (mode urgence / petite quincaillerie)
        p4 = Purchase(
            reference="ACH-2026-00004",
            supplier_id=suppliers_dict["FOUR-004"].id,
            chantier_id=chantier.id,
            date=today - timedelta(days=1),
            status="Reçu",
            payment_status="Payé",
            payment_mode="Espèces",
            subject="Achat direct terrain - Disques et pointes de coffrage",
            notes="Achat d'urgence réglé sur la caisse de chantier.",
            total_amount=84000.0,
            currency="FCFA",
            is_quick_purchase=True,
        )
        db.add(p4)
        db.flush()

        l7 = PurchaseLine(
            purchase_id=p4.id,
            material_id=mat_dict["MAT-2026-009"].id,
            quantity=30.0,
            unit_price=2800.0,
            total_price=84000.0,
            quantity_received=30.0,
        )
        db.add(l7)

        # Entrée en stock magasin chantier pour cet achat rapide
        m7 = StockMovement(
            reference="MVT-2026-00007",
            material_id=mat_dict["MAT-2026-009"].id,
            location_id=loc_dict["DEP-02"].id,
            movement_type="Entrée",
            quantity=30.0,
            unit_price=2800.0,
            chantier_id=chantier.id,
            purchase_id=p4.id,
            date=datetime.now() - timedelta(days=1),
            reason="Achat rapide ACH-2026-00004",
        )
        db.add(m7)

    db.commit()
    print("✅ [SEEDER] Module Achats & Stocks initialisé avec succès !")


def run_all_seeds():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_superadmin(db)
        seed_chantier_types(db)
        seed_responsables(db)
        seed_clients(db)
        seed_planning_and_tasks(db)
        seed_purchases_and_stocks(db)
        print("🎉 [SEEDER] Tous les référentiels, plannings, achats et stocks BTP ont été initialisés avec succès !")
    except Exception as e:
        db.rollback()
        print(f"❌ [SEEDER] Erreur : {e}", file=sys.stderr)
        raise e
    finally:
        db.close()


if __name__ == "__main__":
    run_all_seeds()

