import uuid
from sqlalchemy.orm import Session
from sqlalchemy import text
from app import crud, schemas, models
from app.core.config import settings


def init_sql(db: Session) -> None:
    user = crud.sql.user.read_by_column(
        db, column=models.sql.User.email, value=settings.FIRST_SUPERUSER_USERNAME
    )


    if not user:
        super_user = schemas.sql.UserCreate(
            email=settings.FIRST_SUPERUSER_USERNAME,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_active=True,
            is_superuser=True,
            full_name="Superuser",
        )

        user = crud.sql.user.create(db, obj_in=super_user)
        print(f"Created first super user {super}")
