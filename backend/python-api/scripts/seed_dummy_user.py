import asyncio
import sys
from pathlib import Path

from sqlalchemy import select

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.core.security import hash_password
from app.db.models import AuthIdentity, User
from app.db.session import AsyncSessionLocal

DUMMY_EMAIL = "demo@shoppinglist.dev"
DUMMY_PASSWORD = "DemoPass123!"
DUMMY_DISPLAY_NAME = "Demo User"


async def seed_dummy_user() -> None:
    async with AsyncSessionLocal() as session:
        try:
            user = await session.scalar(select(User).where(User.email == DUMMY_EMAIL))
            if user is None:
                user = User(
                    email=DUMMY_EMAIL,
                    display_name=DUMMY_DISPLAY_NAME,
                    is_active=True,
                )
                session.add(user)
                await session.flush()
                user_created = True
            else:
                user.display_name = DUMMY_DISPLAY_NAME
                user.is_active = True
                user_created = False

            identity = await session.scalar(
                select(AuthIdentity)
                .where(AuthIdentity.user_id == user.id)
                .where(AuthIdentity.provider == "password")
            )
            if identity is None:
                identity = AuthIdentity(
                    user_id=user.id,
                    provider="password",
                    provider_subject=DUMMY_EMAIL,
                    password_hash=hash_password(DUMMY_PASSWORD),
                    email_verified=True,
                )
                session.add(identity)
                identity_created = True
            else:
                identity.provider_subject = DUMMY_EMAIL
                identity.password_hash = hash_password(DUMMY_PASSWORD)
                identity.email_verified = True
                identity_created = False

            await session.commit()

            action = "created" if user_created else "updated"
            identity_action = "created" if identity_created else "updated"
            print(f"Dummy user {action}: {DUMMY_EMAIL}")
            print(f"Password identity {identity_action}.")
            print("Use these credentials for login:")
            print(f"email={DUMMY_EMAIL}")
            print(f"password={DUMMY_PASSWORD}")
        except Exception:
            await session.rollback()
            raise


if __name__ == "__main__":
    asyncio.run(seed_dummy_user())
