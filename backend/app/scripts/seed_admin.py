import os
import sys

from argon2 import PasswordHasher
from sqlalchemy import select

from app.core.db import SessionLocal
from app.models import User
from app.models.enums import UserRole


def main() -> int:
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not email or not password:
        print("ADMIN_EMAIL dan ADMIN_PASSWORD wajib diisi.", file=sys.stderr)
        return 1

    password_hash = PasswordHasher().hash(password)

    with SessionLocal() as db:
        user = db.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(
                email=email,
                name="Admin",
                password_hash=password_hash,
                role=UserRole.admin,
                is_active=True,
            )
            db.add(user)
            action = "dibuat"
        else:
            user.password_hash = password_hash
            user.role = UserRole.admin
            user.is_active = True
            action = "diperbarui"

        db.commit()

    print(f"Admin {email} {action}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
