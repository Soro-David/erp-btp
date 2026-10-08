import os
import re
from datetime import datetime, date
from typing import List, Optional, Tuple
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func, desc, or_

from app.models.chantier import (
    Chantier,
    ChantierType,
    Client,
    Responsable,
    ChantierDocument,
)
from app.schemas.chantier import (
    ChantierCreate,
    ChantierUpdate,
    ChantierTypeCreate,
    ClientCreate,
    ResponsableCreate,
)


class ChantierService:
    def __init__(self, db: Session):
        self.db = db

    # -------------------------------------------------------------------------
    # 1. Code Chantier Auto-Génération
    # -------------------------------------------------------------------------
    def generate_next_code(self) -> Tuple[str, int, int]:
        """
        Génère automatiquement le code chantier suivant au format CH-YYYY-XXX.
        Exemple : CH-2026-001, CH-2026-002.
        """
        current_year = datetime.now().year
        prefix = f"CH-{current_year}-"

        # Recherche de tous les codes débutant par le préfixe de l'année en cours
        existing_chantiers = (
            self.db.query(Chantier.code)
            .filter(Chantier.code.like(f"{prefix}%"))
            .all()
        )

        max_seq = 0
        pattern = re.compile(rf"^CH-{current_year}-(\d+)$")

        for (code,) in existing_chantiers:
            if code:
                match = pattern.match(code.strip())
                if match:
                    try:
                        seq = int(match.group(1))
                        if seq > max_seq:
                            max_seq = seq
                    except ValueError:
                        continue

        next_seq = max_seq + 1
        next_code = f"{prefix}{next_seq:03d}"
        return next_code, current_year, next_seq

    # -------------------------------------------------------------------------
    # 2. Types de Chantier
    # -------------------------------------------------------------------------
    def list_types(self) -> List[ChantierType]:
        return (
            self.db.query(ChantierType)
            .filter(ChantierType.is_active == True)
            .order_by(ChantierType.name.asc())
            .all()
        )

    def create_type(self, type_in: ChantierTypeCreate) -> ChantierType:
        clean_name = type_in.name.strip()
        existing = (
            self.db.query(ChantierType)
            .filter(func.lower(ChantierType.name) == clean_name.lower())
            .first()
        )
        if existing:
            if not existing.is_active:
                existing.is_active = True
                self.db.commit()
                self.db.refresh(existing)
            return existing

        new_type = ChantierType(
            name=clean_name,
            description=type_in.description.strip() if type_in.description else None,
            is_active=True,
        )
        self.db.add(new_type)
        self.db.commit()
        self.db.refresh(new_type)
        return new_type

    # -------------------------------------------------------------------------
    # 3. Clients
    # -------------------------------------------------------------------------
    def list_clients(self) -> List[Client]:
        return self.db.query(Client).order_by(Client.name.asc()).all()

    def create_client(self, client_in: ClientCreate) -> Client:
        client_data = client_in.model_dump()
        new_client = Client(**client_data)
        self.db.add(new_client)
        self.db.commit()
        self.db.refresh(new_client)
        return new_client

    # -------------------------------------------------------------------------
    # 4. Responsables
    # -------------------------------------------------------------------------
    def list_responsables(self, role_name: Optional[str] = None) -> List[Responsable]:
        query = self.db.query(Responsable).filter(Responsable.is_active == True)
        if role_name:
            query = query.filter(func.lower(Responsable.role_name) == role_name.strip().lower())
        return query.order_by(Responsable.last_name.asc(), Responsable.first_name.asc()).all()

    def create_responsable(self, resp_in: ResponsableCreate) -> Responsable:
        # Éviter les doublons stricts (même nom, prénom et rôle)
        existing = (
            self.db.query(Responsable)
            .filter(
                func.lower(Responsable.first_name) == resp_in.first_name.strip().lower(),
                func.lower(Responsable.last_name) == resp_in.last_name.strip().lower(),
                func.lower(Responsable.role_name) == resp_in.role_name.strip().lower(),
            )
            .first()
        )
        if existing:
            if not existing.is_active:
                existing.is_active = True
            if resp_in.phone:
                existing.phone = resp_in.phone
            if resp_in.email:
                existing.email = resp_in.email
            if resp_in.company:
                existing.company = resp_in.company
            self.db.commit()
            self.db.refresh(existing)
            return existing

        new_resp = Responsable(
            first_name=resp_in.first_name.strip(),
            last_name=resp_in.last_name.strip(),
            role_name=resp_in.role_name.strip(),
            phone=resp_in.phone.strip() if resp_in.phone else None,
            email=resp_in.email.strip() if resp_in.email else None,
            company=resp_in.company.strip() if resp_in.company else None,
            is_active=True,
        )
        self.db.add(new_resp)
        self.db.commit()
        self.db.refresh(new_resp)
        return new_resp

    # -------------------------------------------------------------------------
    # 5. Chantiers (Création, Consultation, Liste)
    # -------------------------------------------------------------------------
    def list_chantiers(
        self,
        skip: int = 0,
        limit: int = 100,
        status: Optional[str] = None,
        search: Optional[str] = None,
        include_drafts: bool = True,
    ) -> List[Chantier]:
        query = self.db.query(Chantier)

        if not include_drafts:
            query = query.filter(Chantier.is_draft == False)

        if status and status != "Tous":
            query = query.filter(Chantier.status == status)

        if search:
            search_pattern = f"%{search.strip()}%"
            query = query.filter(
                or_(
                    Chantier.code.ilike(search_pattern),
                    Chantier.name.ilike(search_pattern),
                    Chantier.city.ilike(search_pattern),
                    Chantier.client_name.ilike(search_pattern),
                )
            )

        return query.order_by(desc(Chantier.id)).offset(skip).limit(limit).all()

    def get_chantier_by_id(self, chantier_id: int) -> Optional[Chantier]:
        return self.db.query(Chantier).filter(Chantier.id == chantier_id).first()

    def create_chantier(
        self,
        chantier_in: ChantierCreate,
        current_user_id: Optional[int] = None,
    ) -> Chantier:
        data = chantier_in.model_dump()
        new_client_data = data.pop("new_client", None)

        # 1. Génération ou validation du code
        code = data.get("code")
        if not code or not str(code).strip():
            code, _, _ = self.generate_next_code()
        else:
            code = str(code).strip().upper()
            existing = self.db.query(Chantier).filter(Chantier.code == code).first()
            if existing:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Le code chantier '{code}' est déjà attribué.",
                )
        data["code"] = code

        # 2. Gestion du client (création inline si new_client fourni)
        client_id = data.get("client_id")
        client_name = data.get("client_name")

        if new_client_data and not client_id:
            created_client = self.create_client(ClientCreate(**new_client_data))
            client_id = created_client.id
            client_name = created_client.name
        elif client_id and not client_name:
            c = self.db.query(Client).filter(Client.id == client_id).first()
            if c:
                client_name = c.name

        data["client_id"] = client_id
        data["client_name"] = client_name

        # 3. Synchronisation type de chantier
        type_id = data.get("type_id")
        type_name = data.get("type_name")
        if type_id and not type_name:
            ct = self.db.query(ChantierType).filter(ChantierType.id == type_id).first()
            if ct:
                type_name = ct.name
        data["type_name"] = type_name

        # 4. Calcul automatique de la durée estimée si omise
        start_date = data.get("start_date_planned")
        end_date = data.get("end_date_planned")
        if start_date and end_date and not data.get("estimated_duration_days"):
            data["estimated_duration_days"] = max(0, (end_date - start_date).days)

        data["created_by_id"] = current_user_id

        new_chantier = Chantier(**data)
        self.db.add(new_chantier)
        self.db.commit()
        self.db.refresh(new_chantier)
        return new_chantier

    # -------------------------------------------------------------------------
    # 6. Documents de Chantier
    # -------------------------------------------------------------------------
    def add_document(
        self,
        chantier_id: int,
        document_type: str,
        upload_file: UploadFile,
    ) -> ChantierDocument:
        chantier = self.get_chantier_by_id(chantier_id)
        if not chantier:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Chantier #{chantier_id} non trouvé",
            )

        # Création du dossier cible pour les uploads
        upload_dir = os.path.join(os.getcwd(), "uploads", "chantiers", str(chantier_id))
        os.makedirs(upload_dir, exist_ok=True)

        safe_filename = f"{int(datetime.now().timestamp())}_{upload_file.filename}"
        dest_path = os.path.join(upload_dir, safe_filename)

        # Enregistrement du fichier sur le disque
        file_size = 0
        with open(dest_path, "wb") as buffer:
            while chunk := upload_file.file.read(1024 * 1024):
                file_size += len(chunk)
                buffer.write(chunk)

        doc = ChantierDocument(
            chantier_id=chantier_id,
            document_type=document_type,
            filename=upload_file.filename or safe_filename,
            file_path=dest_path,
            file_size=file_size,
            mime_type=upload_file.content_type,
        )
        self.db.add(doc)
        self.db.commit()
        self.db.refresh(doc)
        return doc
